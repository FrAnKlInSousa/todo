from http import HTTPStatus

import factory.fuzzy
import pytest

from todo.models import Todo, TodoState


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    user_id = 1
    state = factory.fuzzy.FuzzyChoice(TodoState)


@pytest.mark.asyncio
async def test_delete_todo(client, token, session):

    session.add(TodoFactory(user_id=1))

    await session.commit()

    response = client.delete(
        '/todos/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Task has been deleted successfully.'
    }


def test_delete_todo_should_return_not_found(client, token):
    response = client.delete(
        '/todos/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


@pytest.mark.asyncio
async def test_delete_another_user_todo(other_user, token, session, client):
    todo = TodoFactory.build(user_id=other_user.id)
    session.add(todo)
    await session.commit()

    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}
