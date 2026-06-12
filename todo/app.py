from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from todo.database import get_session
from todo.models import User
from todo.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/')
def read_root():
    return {'message': 'Olá mundo!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
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

    user_db = User(**user.model_dump())

    session.add(user_db)

    session.commit()
    session.refresh(user_db)
    return user_db


@app.get('/users/', response_model=UserList)
def read_users(
    limit: int = 10, offset: int = 0, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.put(
    '/users/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            detail='User not found', status_code=HTTPStatus.NOT_FOUND
        )
    try:
        user_db.email = user.email
        user_db.username = user.username
        user_db.password = user.password

        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        return user_db
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already exists',
        )


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            detail='User not found', status_code=HTTPStatus.NOT_FOUND
        )
    session.delete(user_db)
    session.commit()
    return {'message': 'User deleted'}
