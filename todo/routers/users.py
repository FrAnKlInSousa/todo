from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from todo.models import User
from todo.schemas import FilterPage, Message, UserList, UserPublic, UserSchema
from todo.security import create_password_hash, get_current_user, get_session

router = APIRouter(prefix='/users', tags=['users'])

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: Session):

    user_db = await session.scalar(
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

    await session.commit()
    await session.refresh(user_db)
    return user_db


@router.get('/', response_model=UserList)
async def read_users(
    session: Session,
    current_user: CurrentUser,
    filter_users: Annotated[FilterPage, Query()],
):
    users = await session.scalars(
        select(User).limit(filter_users.limit).offset(filter_users.offset)
    )
    return {'users': users}


@router.get('/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK)
async def read_user(
    user_id: int,
    current_user: CurrentUser,
    session: Session,
):
    # todo ver o pq q esse ep falha se colocar o current_user
    user_db = await session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return user_db


@router.put('/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK)
async def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
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
        await session.commit()
        await session.refresh(current_user)
        return current_user
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already exists',
        )


@router.delete('/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    await session.delete(current_user)
    await session.commit()
    return {'message': 'User deleted'}
