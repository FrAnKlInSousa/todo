from http import HTTPStatus


def test_update_user_success(client, user, token):
    response = client.put(
        '/users/1',
        json={
            'username': 'test_edit',
            'password': '122',
            'email': 'user_edit@mail.com',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'test_edit',
        'email': 'user_edit@mail.com',
        'id': 1,
    }


def test_update_user_not_found(client, user, token):
    response = client.put(
        '/users/0',
        json={
            'username': 'test_edit',
            'password': '122',
            'email': 'user_edit@mail.com',
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_update_integrity_error(client, user, token):
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
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or email already exists'}


def test_update_user_with_wrong_user(client, other_user, token):

    response = client.put(
        f'/users/{other_user.id}',
        json={
            'username': 'usertest_updated',
            'email': 'user@test.com',
            'password': 'secret',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
