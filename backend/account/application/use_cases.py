"""Сценарии использования Authentication"""

import random

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
    CacheService,
    MailSender,
    PasswordService,
)


class AuthUseCases:
    def __init__(
        self,
        account_repository: AccountRepository,
        password_service: PasswordService,
        auth_service: AuthService,
        mail_sender: MailSender,
        cache_service: CacheService,
    ):
        self.account_repository = account_repository
        self.password_service = password_service
        self.auth_service = auth_service
        self.mail_sender = mail_sender
        self.cache_service = cache_service

    def register(self, email: str, username: str, password: str) -> bool:
        exist = self.account_repository.get_by_email(email)
        if exist:
            raise AccountAlreadyExist('Аккаунт с таким email уже существует')
        code = random.randint(100000, 999999)
        password_hash = self.password_service.hash_password(password)
        account = Account(
            email=email,
            username=username,
            password_hash=password_hash,
            is_active=True,
        )
        self.cache_service.post_confirmation_code(account, code)
        self.mail_sender.send_code(code, email)
        return True

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

    def mail_confirmation(self, email: str, enter_code: int) -> bool:
        info = self.cache_service.get_info_by_email(email)
        if info is None:
            return False
        saved_code = info['code']
        if enter_code != saved_code:
            return False
        exist = self.account_repository.get_by_email(email)
        if exist:
            raise AccountAlreadyExist('Аккаунт с таким email уже существует')
        account = Account(
            email=email,
            username=info['username'],
            password_hash=info['password_hash'],
            is_active=True,
        )
        account = self.account_repository.save(account)
        return self.cache_service.delete_by_email(email)
