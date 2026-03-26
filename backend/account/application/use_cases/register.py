import random

from account.application.exceptions import AccountAlreadyExist
from account.domain.entities import Account
from account.domain.ports import (
    AccountRepository,
    CacheService,
    MailSender,
    PasswordService,
)


def register(
    account_repository: AccountRepository,
    password_service: PasswordService,
    mail_sender: MailSender,
    cache_service: CacheService,
    email: str,
    username: str,
    password: str,
) -> bool:
    exist = account_repository.get_by_email(email)
    if exist:
        raise AccountAlreadyExist('Аккаунт с таким email уже существует')
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
