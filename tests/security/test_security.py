from http import HTTPStatus

from jwt import decode

from todo.security import (
    create_access_token,
)


def test_jwt(settings):
    data = {'test': 'test'}

    token = create_access_token(data)

    decoded = decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client, user):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': 'Bearer token invalido'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_with_no_subject(client):
    token = create_access_token({'no-email': 'test'})
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_with_no_user(client):
    data = {'sub': 'not_found@mail.com'}

    token = create_access_token(data)
    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

    assert response.json() == {'detail': 'Could not validate credentials'}
