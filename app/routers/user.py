from typing import List
from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.get(
    '/me',
    response_model=schemas.UserProfileTable
)
# @router.get('/')
def get_current_user(
    current_user: int = Depends(oauth2.get_current_user)
):
    return current_user
    # return current_user


@ router.get('/all', response_model=List[schemas.UserProfileTable])
# @router.get('/')
def get_users(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    if current_user.role_id != 1 or current_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    results = db.query(models.UserProfile).all()
    return results


@ router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Inserting a new user into the database
    """
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    input_data = user.dict()

    db_user = db.query(models.UserLogin).filter(
        models.UserLogin.email_address == input_data['email_address']).first()

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Failed to create the user record. Reason: email exists in the DB"
        )

    user_profile = models.UserProfile(
        user_name=input_data['user_name'],
        phone_number=input_data['phone_number'],
        residential_address=input_data['residential_address'],
        books_allowed=input_data['books_allowed'],
        role_id=input_data['role_id']
    )
    db.add(user_profile)
    db.commit()
    db.refresh(user_profile)

    user_profile_id = user_profile.__dict__['user_profile_id']

    print(user_profile_id)
    user_login = models.UserLogin(
        user_profile_id=user_profile_id,
        email_address=input_data['email_address'],
        password=input_data['password']
    )
    db.add(user_login)
    db.commit()
    db.refresh(user_login)

    new_user = {
        "user_profile_id": user_profile_id,
        "user_name":  input_data['user_name'],
        "email_address": user_login.__dict__['email_address'],
        "created_at": user_login.__dict__['created_at']
    }

    return new_user


@router.get(
    '/info/{id}',
    response_model=schemas.UserProfileTable
)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    if current_user.role_id != 1 or current_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    user = db.query(
        models.UserProfile
    ).filter(
        models.UserProfile.user_profile_id == id
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist!"
        )
    return user
