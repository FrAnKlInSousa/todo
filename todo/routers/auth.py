from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from todo.models import User
from todo.schemas import Token
from todo.security import create_access_token, get_session, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])

Session = Annotated[Session, Depends(get_session)]
OAuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', status_code=HTTPStatus.OK, response_model=Token)
def login_for_access_token(
    session: Session,
    form_data: OAuthForm,
):
    user_db = session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )
    if not verify_password(form_data.password, user_db.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )
    data = {'sub': user_db.email}
    token = create_access_token(data)
    return {'access_token': token, 'token_type': 'Bearer'}
