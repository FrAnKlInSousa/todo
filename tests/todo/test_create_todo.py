from http import HTTPStatus


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
