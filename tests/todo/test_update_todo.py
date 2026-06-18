from http import HTTPStatus

import pytest

from tests.factories.todo_factory import TodoFactory


def test_update_inexistent_todo(client, token):
    response = client.patch(
        '/todos/0', headers={'Authorization': f'Bearer {token}'}, json={}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


@pytest.mark.asyncio
async def test_update_another_user_todo(client, other_user, session, token):
    todo = TodoFactory.build(user_id=other_user.id)
    session.add(todo)
    await session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


@pytest.mark.asyncio
async def test_update_todo(token, session, client, user):
    todo = TodoFactory.build(user_id=user.id)
    session.add(todo)
    await session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'new title'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'new title'
