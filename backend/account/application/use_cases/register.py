import random

from account.application.exceptions import (
    AccountAlreadyExist,
    UsernameAlreadyExist,
)
from account.application.interfaces.cache_service import CacheService
from account.application.interfaces.mail_sender import MailSender
from account.application.interfaces.password_service import PasswordService
from account.application.interfaces.uow import UnitOfWork
from account.domain.entities import Account


def register(
    uow: UnitOfWork,
    password_service: PasswordService,
    mail_sender: MailSender,
    cache_service: CacheService,
    email: str,
    username: str,
    password: str,
) -> bool:
    with uow:
        exist_by_email = uow.accounts.get_by_email(email)
        exist_by_username = uow.accounts.get_by_username(username)

        if exist_by_email:
            raise AccountAlreadyExist('Аккаунт с таким email уже существует')
        if exist_by_username:
            raise UsernameAlreadyExist(
                'Аккаунт с таким username уже существует'
            )

        code = random.randint(100000, 999999)
        password_hash = password_service.hash_password(password)

        account = Account(
            id=None,
            email=email,
            username=username,
            password_hash=password_hash,
            is_active=True,
        )

        cache_service.post_confirmation_code(account, code)
        mail_sender.send_code(code, email)

    return True
