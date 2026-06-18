from http import HTTPStatus

import pytest

from tests.factories.todo_factory import TodoFactory
from todo.models import Todo


@pytest.mark.asyncio
async def test_should_filter_by_state_and_list_3_todos(client, token, session):
    expected_len = 3
    session.add_all(TodoFactory.create_batch(5, state='todo'))
    session.add_all(TodoFactory.create_batch(3, state='draft'))

    await session.commit()

    response = client.get(
        '/todos/?state=draft', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_len


@pytest.mark.asyncio
async def test_should_filter_by_title_and_list_4_todos(client, token, session):
    expected_len = 4
    session.add_all(TodoFactory.create_batch(5))
    session.add_all(TodoFactory.create_batch(4, title='meu título'))

    await session.commit()

    response = client.get(
        '/todos/?title=meu título',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_len


@pytest.mark.asyncio
async def test_should_filter_description_and_list_5_todos(
    client, session, token
):
    expected_len = 5
    session.add_all(TodoFactory.create_batch(5))
    session.add_all(TodoFactory.create_batch(5, description='minha descrição'))

    await session.commit()

    response = client.get(
        '/todos/?description=minha desc',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_len


@pytest.mark.asyncio
async def test_should_return_all_todo_fields(
    client, token, user, session, mock_db_time
):
    with mock_db_time(model=Todo) as time:
        todo = TodoFactory(user_id=user.id)
        session.add(todo)
        await session.commit()
        await session.refresh(todo)

        response = client.get(
            '/todos', headers={'Authorization': f'Bearer {token}'}
        )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'todos': [
            {
                'created_at': time.isoformat(),
                'updated_at': time.isoformat(),
                'description': todo.description,
                'id': todo.id,
                'state': todo.state,
                'title': todo.title,
                'user_id': todo.user_id,
            }
        ]
    }
