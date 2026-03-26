import pytest
from fastapi.testclient import TestClient
from typing import Callable, Generator

from account.application.use_cases import AuthUseCases
from account.domain.entities import Account
from app.api import auth_routes
from app.api.main import app
from app.config import settings


class FakeAccountRepository:
    def __init__(self) -> None:
        self._accounts_by_email: dict[str, Account] = {}
        self._next_id = 1

    def get_by_id(self, id: int):
        for acc in self._accounts_by_email.values():
            if acc.id == id:
                return acc
        return None

    def get_by_email(self, email: str):
        return self._accounts_by_email.get(email.strip().lower())

    def save(self, account: Account) -> Account:
        email = account.email.strip().lower()
        if account.id is None:
            account.id = self._next_id
            self._next_id += 1

        saved = Account(
            id=account.id,
            email=account.email,
            username=account.username,
            password_hash=account.password_hash,
            is_active=account.is_active,
        )
        self._accounts_by_email[email] = saved
        return saved


class FakePasswordService:
    @staticmethod
    def hash_password(password: str) -> str:
        return f'hash:{password}'

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        return hashed_password == f'hash:{password}'


class FakeAuthService:
    def __init__(self, secret: str, algorithm: str) -> None:
        self.secret = secret
        self.algorithm = algorithm

    def create_token_pair(self, account_id: int) -> dict:
        return {
            'access_token': f'access:{account_id}',
            'refresh_token': f'refresh:{account_id}',
            'token_type': 'Bearer',
            'expires_in': 900,
        }

    def refresh_token_pair(self, refresh_token: str) -> dict:
        raise NotImplementedError

    def get_payload(self, access_token: str) -> dict:
        raise NotImplementedError


class FakeMailSender:
    def send_code(self, code: int, to_email: str) -> None:
        return None


class FakeCacheService:
    def __init__(self) -> None:
        self._by_email: dict[str, dict] = {}

    def post_confirmation_code(self, account: Account, code: int) -> None:
        self._by_email[account.email.strip().lower()] = {
            'username': account.username,
            'password_hash': account.password_hash,
            'code': code,
        }

    def get_info_by_email(self, email: str):
        return self._by_email.get(email.strip().lower())

    def delete_by_email(self, email: str) -> bool:
        key = email.strip().lower()
        return self._by_email.pop(key, None) is not None


@pytest.fixture()
def fixed_confirmation_code() -> int:
    return 123456

@pytest.fixture()
def api_url() -> Callable[[str], str]:
    def _api_url(path_suffix: str) -> str:
        base_prefix = '/' + settings.base_url.strip('/')
        return f'{base_prefix}{path_suffix}'

    return _api_url

@pytest.fixture()
def auth_use_cases(monkeypatch: pytest.MonkeyPatch, fixed_confirmation_code: int) -> AuthUseCases:
    import account.application.use_cases as use_cases_module

    monkeypatch.setattr(use_cases_module.random, 'randint', lambda _a, _b: fixed_confirmation_code)

    repo = FakeAccountRepository()
    cache = FakeCacheService()
    return AuthUseCases(
        account_repository=repo,
        password_service=FakePasswordService,
        auth_service=FakeAuthService(settings.secret, settings.algorithm),
        mail_sender=FakeMailSender(),
        cache_service=cache,
    )

@pytest.fixture()
def client(auth_use_cases: AuthUseCases) -> Generator[TestClient, None, None]:
    app.dependency_overrides[auth_routes.get_auth_use_cases] = (lambda: auth_use_cases)
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.pop(auth_routes.get_auth_use_cases, None)

@pytest.fixture()
def registered_user(client, api_url, fixed_confirmation_code):
    def _create_user(email: str, username: str, password: str = "StrongPassword123"):

        register_resp = client.post(
            api_url('/auth/registry'),
            json={
                'email': email, 
                'username': username, 
                'password': password
                }
            )
        assert register_resp.status_code == 200

        confirm_resp = client.post(
            api_url('/auth/confirm_email'),
            json={
                'email': email, 
                'code': fixed_confirmation_code
                }
            )
        assert confirm_resp.status_code == 200

        login_resp = client.post(
            api_url('/auth/login'), 
            json={
                'email': email, 
                'username': username,
                'password': password
                }
            )
        assert login_resp.status_code == 200
        token = login_resp.json()['access_token']
        
        return {
            'email': email,
            'username': username,
            'password': password,
            'access_token': token
        }
    return _create_user