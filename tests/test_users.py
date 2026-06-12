from http import HTTPStatus

from todo.schemas import UserPublic


def test_create_user_success(client):
    response = client.post(
        '/users/',
        json={'username': 'test', 'password': '', 'email': 'user@mail.com'},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'test',
        'email': 'user@mail.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    response = client.get('/users/')
    user_schema = UserPublic.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user_success(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'test_edit',
            'password': '122',
            'email': 'user_edit@mail.com',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'test_edit',
        'email': 'user_edit@mail.com',
        'id': 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/0',
        json={
            'username': 'test_edit',
            'password': '122',
            'email': 'user_edit@mail.com',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user_success(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/0')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_integrity_error(client, user):
    client.post(
        '/users/',
        json={
            'username': 'ana',
            'email': 'ana@email.com',
            'password': 'senha123',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'ana',
            'email': 'asd@email.com',
            'password': 'senha123',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or email already exists'}
