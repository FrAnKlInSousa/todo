from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from todo.models import User
from todo.schemas import Message, UserList, UserPublic, UserSchema
from todo.security import create_password_hash, get_current_user, get_session

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):

    user_db = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    # todo verificar caso passe ana@mail (sem o .com), pois não estava dando
    #  erro no test_update_integrity_error

    if user_db:
        raise HTTPException(
            detail='Email or username already exists.',
            status_code=HTTPStatus.CONFLICT,
        )

    user_db = User(
        username=user.username,
        email=user.email,
        password=create_password_hash(user.password),
    )

    session.add(user_db)

    session.commit()
    session.refresh(user_db)
    return user_db


@router.get('/', response_model=UserList)
def read_users(
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@router.get('/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return user_db


@router.put('/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    try:
        current_user.email = user.email
        current_user.username = user.username
        current_user.password = create_password_hash(user.password)

        session.add(current_user)
        session.commit()
        session.refresh(current_user)
        return current_user
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already exists',
        )


@router.delete('/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    session.delete(current_user)
    session.commit()
    return {'message': 'User deleted'}
