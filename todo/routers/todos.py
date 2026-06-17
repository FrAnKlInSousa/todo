from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from todo.database import get_session
from todo.models import Todo, User
from todo.schemas import TodoPublic, TodoSchema
from todo.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TodoPublic, status_code=HTTPStatus.CREATED)
async def create_todo(todo: TodoSchema, session: Session, user: CurrentUser):
    db_todo = Todo(**todo.model_dump(), user_id=user.id)

    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    return db_todo
