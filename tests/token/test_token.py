from http import HTTPStatus


def test_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_token_with_not_found_user(client):
    response = client.post(
        '/auth/token',
        data={'username': 'unexistent@example.com', 'password': 'password'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_token_wrong_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'wrongpassword'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
