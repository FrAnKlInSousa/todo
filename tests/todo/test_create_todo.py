from http import HTTPStatus

import pytest
from sqlalchemy import select
from sqlalchemy.exc import DataError, PendingRollbackError

from tests.factories.todo_factory import TodoFactory
from todo.models import Todo, User


def test_create_todo(client, token, mock_db_time):
    with mock_db_time(model=Todo) as time:
        response = client.post(
            '/todos',
            json={
                'title': 'title',
                'description': 'description',
                'state': 'todo',
                'id': 1,
            },
            headers={'Authorization': f'Bearer {token}'},
        )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'title': 'title',
        'description': 'description',
        'state': 'todo',
        'id': 1,
        'user_id': 1,
        'created_at': time.isoformat(),
        'updated_at': time.isoformat(),
    }


@pytest.mark.asyncio
async def test_should_create_5_todos(client, session, token):

    expected_todos = 5
    session.add_all(TodoFactory.create_batch(5))
    await session.commit()

    response = client.get(
        '/todos', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_create_todo_error(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='test',
        user_id=user.id,
    )

    session.add(todo)

    with pytest.raises(DataError):
        await session.commit()

    with pytest.raises(PendingRollbackError):
        await session.scalar(select(Todo))


def test_should_rise_error_on_todo_create_with_invalid_state(client, token):
    response = client.post(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test Todo',
            'description': 'Test Desc',
            'state': 'test',
        },
    )
    response_message = response.json()['detail'][0]['msg']
    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert (
        response_message
        == "Input should be 'draft', 'todo', 'doing', 'done' or 'trash'"
    )
