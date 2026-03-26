import random

from account.application.exceptions import AccountAlreadyExist, UsernameAlreadyExist
from account.domain.entities import Account
from account.application.interfaces import (
    CacheService,
    MailSender,
    PasswordService,
)
from account.domain.ports.account_repository import AccountRepository


def register(
    account_repository: AccountRepository,
    password_service: PasswordService,
    mail_sender: MailSender,
    cache_service: CacheService,
    email: str,
    username: str,
    password: str,
) -> bool:
    exist_by_email = account_repository.get_by_email(email)
    exist_by_username = account_repository.get_by_username(username)
    if exist_by_email:
        raise AccountAlreadyExist('Аккаунт с таким email уже существует')
    if exist_by_username:
        raise UsernameAlreadyExist('Аккаунт с таким username уже существует')
    code = random.randint(100000, 999999)
    password_hash = password_service.hash_password(password)
    account = Account(
        email=email,
        username=username,
        password_hash=password_hash,
        is_active=True,
    )
    cache_service.post_confirmation_code(account, code)
    mail_sender.send_code(code, email)
    return True
