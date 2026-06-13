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


def test_create_user_with_same_email(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'joao',
            'email': 'test@mail.com',
            'password': 'secret123',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email or username already exists.'}


def test_create_user_with_same_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'user_test',
            'email': 'joao@mail.com',
            'password': 'secret123',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email or username already exists.'}
