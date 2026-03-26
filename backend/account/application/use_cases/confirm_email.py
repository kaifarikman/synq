from account.application.exceptions import (
    AccountAlreadyExist,
    AccountHasNoId,
)
from account.domain.entities import Account
from account.domain.ports import AccountRepository, CacheService
from profile.application.use_cases import create_profile
from profile.domain.ports import ProfileRepository


def confirm_email(
    account_repository: AccountRepository,
    cache_service: CacheService,
    profile_repository: ProfileRepository,
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
    account = account_repository.save(account)
    if account.id is None:
        raise AccountHasNoId('У аккаунта нет id')

    create_profile(
        profile_repository=profile_repository,
        user_id=account.id,
    )
    return cache_service.delete_by_email(email)
