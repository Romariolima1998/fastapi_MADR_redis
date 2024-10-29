
from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        '/auth/token/',
        data={'username': user.username, 'password': user.clean_password}

    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_token_wrong_username(client, user):
    response = client.post(
        '/auth/token/',
        data={'username': 'wrong_username', 'password': user.clean_password}

    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_token_wrong_password(client, user):
    response = client.post(
        '/auth/token/',
        data={'username': user.username, 'password': 'wrong_password'}

    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_token_expired_after_time(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token/',
            data={'username': user.username, 'password': user.clean_password}
        )
        token = response.json()
        assert response.status_code == HTTPStatus.OK

    with freeze_time('2023-07-14 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'authorization': f'Bearer {token}'},
            json={
                'username': 'test2',
                'email': 'test@test.com',
                'password': 'test',
            }
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_refresh_token(client, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'authorization': f'Bearer {token}'}
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_refresh_token_with_token_expired(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token/',
            data={'username': user.username, 'password': user.clean_password}
        )
        token = response.json()
        assert response.status_code == HTTPStatus.OK

    with freeze_time('2023-07-14 12:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'authorization': f'Bearer {token}'}
        )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
