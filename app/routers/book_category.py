from datetime import datetime
from fastapi import status, HTTPException, Response, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, oauth2

# Using hyphen by following this answer
# https://stackoverflow.com/a/18449772
router = APIRouter(
    prefix='/book-category',
    tags=['Book Category']
)


@router.get(
    '/all',
    response_model=List[schemas.BookCategory]
)
# @router.get('/')
def get_book_categorys(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    # Allowing only the admins to proceed
    if current_user.role_id != 1 or current_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    results = db.query(models.BookCategory).all()
    return results


@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.BookCategory,
)
def create_book_category(
    book_category: schemas.BookCategoryCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    # Allowing only the admins to proceed
    if current_user.role_id != 1 or current_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    new_book_category = models.BookCategory(**book_category.dict())
    # ** unpacks the dictionary into this format:
    # title=post.title, content=post.content, ...
    # This prevents us from specifiying individual fields

    db.add(new_book_category)
    db.commit()
    db.refresh(new_book_category)

    return new_book_category


@router.get(
    '/info/{id}',
    response_model=schemas.BookCategory
)
def get_book_category(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    """ 
    {id} is a path parameter
    """
    # We are
    # - taking an string from the parameter
    # - converting it to int
    # - then again converting it to str
    # We are doing this because we want to valid that the user is giving
    # only integers in the argument and not string like `adfadf`.
    # Plus we are adding a comma after the str(id) because we run into an
    # error later. Don't know the reason for the error yet.
    # post = cursor.fetchone()

    if current_user.role_id != 1 or current_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    book_category = db.query(models.BookCategory).filter(
        models.BookCategory.book_category_id == id
    ).first()

    if not book_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book Category with id: {id} not found!"
        )

    return book_category


@router.delete(
    '/delete/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_book_category(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    if current_user.role_id != 1 or current_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    book_category_query = db.query(
        models.BookCategory
    ).filter(
        models.BookCategory.book_category_id == id
    )
    book_category = book_category_query.first()

    if book_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book Category with id: {id} does not exist!"
        )

    book_category_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# make sure to add some body in the postman to check it.
@router.put(
    '/update/{id}',
    response_model=schemas.BookCategoryCreate
)
def update_book_category(
    id: int,
    updated_book_category: schemas.BookCategoryCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    if current_user.role_id != 1 or current_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    book_category_query = db.query(
        models.BookCategory
    ).filter(
        models.BookCategory.book_category_id == id
    )

    book_category = book_category_query.first()

    if book_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book Category with id: {id} does not exist!"
        )

    # print(book_category.__dict__)
    updated_init_type = updated_book_category.dict()

    # print(updated_init_type)
    book_category_query.update(
        updated_init_type,
        synchronize_session=False
    )
    db.commit()

    # Sending the updated book category back to the user
    return book_category_query.first()
