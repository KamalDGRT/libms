from datetime import datetime
from fastapi import status, HTTPException, Response, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, oauth2

# Using hyphen by following this answer
# https://stackoverflow.com/a/18449772
router = APIRouter(
    prefix='/book-transaction',
    tags=['Book Transaction']
)


@router.get(
    '/all',
    response_model=List[schemas.BookTransaction],
)
# @router.get('/')
def get_books(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    results = db.query(models.BookTransaction).all()
    return results


@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.BookTransactionSimple,
)
def initiate_book_transaction(
    book: schemas.BookTransactionCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    # Allowing only the admins to proceed

    if current_user.role_id != 1 or current_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    books = book.dict()["books"]

    new_book_transaction = models.BookTransaction(
        borrowed_by=current_user.user_profile_id
    )
    db.add(new_book_transaction)
    db.commit()
    db.refresh(new_book_transaction)

    trn_id = new_book_transaction.__dict__["book_transaction_id"]

    new_books = []
    for trn_book in books:
        book_borrowed = models.BookBorrow(
            book_id=trn_book["book_id"],
            book_transaction_id=trn_id
        )
        db.add(book_borrowed)
        db.commit()
        db.refresh(book_borrowed)
        new_books.append(book_borrowed.__dict__)

    return {"book_transaction_id": trn_id, "books": new_books}


@router.get(
    '/info/{id}',
    response_model=schemas.BookTransaction
)
def get_book_transaction_info(
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

    book = db.query(models.BookTransaction).filter(
        models.BookTransaction.book_transaction_id == id
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

    book_transaction_query = db.query(
        models.BookTransaction
    ).filter(
        models.BookTransaction.book_transaction_id == id
    )
    book = book_transaction_query.first()

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {id} does not exist!"
        )

    book_transaction_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# make sure to add some body in the postman to check it.
@router.put(
    '/update/{id}',
    response_model=schemas.BookTransaction
)
def update_book(
    id: int,
    updated_book_transaction: schemas.BookTransactionCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    if current_user.role_id != 1 or current_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    book_transaction_query = db.query(
        models.BookTransaction
    ).filter(
        models.BookTransaction.book_transaction_id == id
    )

    book = book_transaction_query.first()

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book Transaction with id: {id} does not exist!"
        )

    # print(status_code.__dict__)
    updated_book_transaction_info = updated_book_transaction.dict()

    # print(updated_init_type)
    book_transaction_query.update(
        updated_book_transaction_info,
        synchronize_session=False
    )
    db.commit()

    # Sending the updated empl_type back to the user
    return book_transaction_query.first()
