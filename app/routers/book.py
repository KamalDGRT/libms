from datetime import datetime
from fastapi import status, HTTPException, Response, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, oauth2

# Using hyphen by following this answer
# https://stackoverflow.com/a/18449772
router = APIRouter(
    prefix='/book',
    tags=['Book']
)


@router.get(
    '/all',
    response_model=List[schemas.BookSimple],
)
# @router.get('/')
def get_books(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    results = db.query(models.Book).all()
    return results


@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.BookSimple,
)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    # Allowing only the admins to proceed
    if current_user.role_id != 1 or current_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    new_book = models.Book(**book.dict())
    # ** unpacks the dictionary into this format:
    # title=post.title, content=post.content, ...
    # This prevents us from specifiying individual fields

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


@router.get(
    '/info/{id}',
    response_model=schemas.BookComplete
)
def get_book(
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

    book = db.query(models.Book).filter(
        models.Book.book_id == id
    ).first()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {id} not found!"
        )

    return book


@router.delete(
    '/delete/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_book(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    if current_user.role_id != 1 or current_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    book_query = db.query(
        models.Book
    ).filter(
        models.Book.book_id == id
    )
    book = book_query.first()

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {id} does not exist!"
        )

    book_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# make sure to add some body in the postman to check it.
@router.put(
    '/update/{id}',
    response_model=schemas.BookCreate
)
def update_book(
    id: int,
    updated_book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    if current_user.role_id != 1 or current_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    book_query = db.query(
        models.Book
    ).filter(
        models.Book.book_id == id
    )

    book = book_query.first()

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {id} does not exist!"
        )

    # print(status_code.__dict__)
    updated_book = updated_book.dict()

    # print(updated_init_type)
    book_query.update(
        updated_book,
        synchronize_session=False
    )
    db.commit()

    # Sending the updated empl_type back to the user
    return book_query.first()
