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
    session.add_all(TodoFactory.create_batch(5, description='minha'))

    await session.commit()

    response = client.get(
        '/todos/?description=min',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_len
