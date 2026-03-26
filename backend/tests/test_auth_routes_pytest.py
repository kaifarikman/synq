import pytest

from account.application.exceptions import (
    AccountAlreadyExist,
    AccountIsDeactivate,
    AccountNotFound,
    InvalidPassword,
    UsernameAlreadyExist,
)


def test_registry_returns_true(client, auth_use_cases) -> None:
    response = client.post(
        '/api/v1/auth/registry',
        json={
            'email': 'new@example.com',
            'username': 'new-user',
            'password': 'secret',
        },
    )

    assert response.status_code == 200
    assert response.json() is True
    assert auth_use_cases.register_calls == [
        ('new@example.com', 'new-user', 'secret'),
    ]


@pytest.mark.parametrize(
    ('error', 'detail'),
    [
        (
            AccountAlreadyExist('Аккаунт с таким email уже существует'),
            'Аккаунт с таким email уже существует',
        ),
        (
            UsernameAlreadyExist('Аккаунт с таким username уже существует'),
            'Аккаунт с таким username уже существует',
        ),
    ],
)
def test_registry_maps_conflicts_to_409(
    client,
    auth_use_cases,
    error: Exception,
    detail: str,
) -> None:
    auth_use_cases.register_error = error

    response = client.post(
        '/api/v1/auth/registry',
        json={
            'email': 'new@example.com',
            'username': 'new-user',
            'password': 'secret',
        },
    )

    assert response.status_code == 409
    assert response.json() == {'detail': detail}


def test_confirm_email_returns_true(client, auth_use_cases) -> None:
    response = client.post(
        '/api/v1/auth/confirm_email',
        json={'email': 'user@example.com', 'code': 123456},
    )

    assert response.status_code == 200
    assert response.json() is True
    assert auth_use_cases.confirmation_calls == [('user@example.com', 123456)]


def test_confirm_email_returns_400_for_invalid_code(
    client,
    auth_use_cases,
) -> None:
    auth_use_cases.confirmation_response = False

    response = client.post(
        '/api/v1/auth/confirm_email',
        json={'email': 'user@example.com', 'code': 123456},
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Неверный код подтверждения'}


def test_confirm_email_returns_409_for_existing_account(
    client,
    auth_use_cases,
) -> None:
    auth_use_cases.confirmation_error = AccountAlreadyExist(
        'Аккаунт с таким email уже существует'
    )

    response = client.post(
        '/api/v1/auth/confirm_email',
        json={'email': 'user@example.com', 'code': 123456},
    )

    assert response.status_code == 409
    assert response.json() == {
        'detail': 'Аккаунт с таким email уже существует',
    }


def test_login_returns_token_pair(client, auth_use_cases) -> None:
    response = client.post(
        '/api/v1/auth/login',
        json={'email': 'user@example.com', 'password': 'secret'},
    )

    assert response.status_code == 200
    assert response.json() == auth_use_cases.login_response
    assert auth_use_cases.login_calls == [('user@example.com', 'secret')]


@pytest.mark.parametrize(
    ('error', 'status_code'),
    [
        (AccountNotFound('Не существует аккаунта с таким email'), 400),
        (InvalidPassword('Неверный email или пароль'), 400),
        (AccountIsDeactivate('Аккаунт деактивирован'), 403),
    ],
)
def test_login_maps_domain_errors(
    client,
    auth_use_cases,
    error: Exception,
    status_code: int,
) -> None:
    auth_use_cases.login_error = error

    response = client.post(
        '/api/v1/auth/login',
        json={'email': 'user@example.com', 'password': 'secret'},
    )

    assert response.status_code == status_code
    assert response.json() == {'detail': str(error)}


def test_me_requires_bearer_token(client) -> None:
    response = client.get('/api/v1/auth/me')

    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Токен отсутствует или недействителен',
    }


def test_me_returns_current_user(client) -> None:
    response = client.get(
        '/api/v1/auth/me',
        headers={'Authorization': 'Bearer access-token'},
    )

    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'email': 'user@example.com',
        'username': 'user',
    }


@pytest.mark.parametrize(
    'error',
    [
        AccountNotFound('Пользователь не найден'),
        ValueError('bad token'),
    ],
)
def test_me_returns_401_for_invalid_token(
    client,
    auth_use_cases,
    error: Exception,
) -> None:
    auth_use_cases.current_user_error = error

    response = client.get(
        '/api/v1/auth/me',
        headers={'Authorization': 'Bearer access-token'},
    )

    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Токен отсутствует или недействителен',
    }


def test_logout_returns_204(client, auth_use_cases) -> None:
    response = client.post(
        '/api/v1/auth/logout',
        headers={'Authorization': 'Bearer access-token'},
    )

    assert response.status_code == 204
    assert response.content == b''
    assert auth_use_cases.logout_calls == ['access-token']


def test_logout_returns_401_for_invalid_token(
    client,
    auth_use_cases,
) -> None:
    auth_use_cases.logout_error = ValueError('bad token')

    response = client.post(
        '/api/v1/auth/logout',
        headers={'Authorization': 'Bearer access-token'},
    )

    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Токен отсутствует или недействителен',
    }
