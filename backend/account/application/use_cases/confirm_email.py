from account.application.exceptions import AccountAlreadyExist
from account.domain.entities import Account
from account.domain.ports import AccountRepository, CacheService


def confirm_email(
    account_repository: AccountRepository,
    cache_service: CacheService,
    email: str,
    enter_code: int,
) -> bool:
    info = cache_service.get_info_by_email(email)
    if info is None:
        return False
    saved_code = info['code']
    if enter_code != saved_code:
        return False
    exist = account_repository.get_by_email(email)
    if exist:
        raise AccountAlreadyExist('Аккаунт с таким email уже существует')
    account = Account(
        email=email,
        username=info['username'],
        password_hash=info['password_hash'],
        is_active=True,
    )
    account_repository.save(account)
    return cache_service.delete_by_email(email)
