from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from todo.database import get_session
from todo.models import Todo, User
from todo.schemas import FilterTodo, TodoList, TodoPublic, TodoSchema
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


@router.get('/', response_model=TodoList, status_code=HTTPStatus.OK)
async def list_todos(
    user: CurrentUser,
    session: Session,
    todo_filter: Annotated[FilterTodo, Query()],
):
    query = select(Todo).where(Todo.user_id == user.id)
    if todo_filter.state:
        query = query.filter(Todo.state == todo_filter.state)

    if todo_filter.title:
        query = query.filter(Todo.title.contains(todo_filter.title))

    if desc := todo_filter.description:  # exemplo com operador walrus
        query = query.filter(Todo.description.contains(desc))

    todos = await session.scalars(
        query.limit(todo_filter.limit).offset(todo_filter.offset)
    )

    return {'todos': todos.all()}
