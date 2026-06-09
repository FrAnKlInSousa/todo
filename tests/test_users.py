from http import HTTPStatus


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


def test_read_users_success(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'test',
                'email': 'user@mail.com',
                'id': 1,
            }
        ]
    }


def test_update_user_success(client):
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


def test_delete_user_success(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'test_edit',
        'email': 'user_edit@mail.com',
        'id': 1,
    }


def test_delete_user_not_found(client):
    response = client.delete('/users/0')
    assert response.status_code == HTTPStatus.NOT_FOUND
