from http import HTTPStatus

import pytest

from tests.factories.todo_factory import TodoFactory


def test_create_todo(client, token):
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
