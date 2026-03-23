"""Сценарии использования Authentication"""

from account.application.exceptions import (
    AccountAlreadyExist,
    AccountHasNoId,
    AccountIsDeactivate,
    AccountNotFound,
    InvalidPassword,
)
from account.domain.entities import Account
from account.domain.repositories import (
    AccountRepository,
    AuthService,
    PasswordService,
)


class AuthUseCases:
    def __init__(
        self,
        account_repository: AccountRepository,
        password_service: PasswordService,
        auth_service: AuthService,
    ):
        self.account_repository = account_repository
        self.password_service = password_service
        self.auth_service = auth_service

    def resigtry(self, email: str, password: str) -> Account:
        exist = self.account_repository.get_by_email(email)
        if exist:
            raise AccountAlreadyExist('Аккаунт с таким email уже существует')
        account = Account(
            email=email,
            password_hash=self.password_service.hash_password(password),
            is_active=True,
        )
        account = self.account_repository.save(account)
        return account

    def login(self, email: str, password: str) -> dict:
        user = self.account_repository.get_by_email(email)
        if not user:
            raise AccountNotFound('Не существует аккаунта с таким email')
        if not user.can_login:
            raise AccountIsDeactivate('Аккаунт деактивирован')
        if not self.password_service.check_password(
            password, user.password_hash
        ):
            raise InvalidPassword('Неверный email или пароль')
        if user.id is None:
            raise AccountHasNoId('У аккаунта нет id')
        return self.auth_service.create_token_pair(user.id)
