from profile.domain.entities import Profile
from uuid import uuid4

from account.application.exceptions import (
    AccountAlreadyExist,
    AccountHasNoId,
)
from account.application.interfaces.cache_service import CacheService
from account.application.interfaces.uow import UnitOfWork
from account.domain.entities import Account


def confirm_email(
    uow: UnitOfWork,
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

    with uow:
        exist = uow.accounts.get_by_email(email)
        if exist:
            raise AccountAlreadyExist('Аккаунт с таким email уже существует')

        account = Account(
            id=None,
            email=email,
            username=info['username'],
            password_hash=info['password_hash'],
            is_active=True,
        )

        account = uow.accounts.save(account)

        if account.id is None:
            raise AccountHasNoId('У аккаунта нет id')

        profile = Profile(
            user_id=account.id,
            uuid=uuid4(),
        )
        uow.profiles.save(save_profile=profile)

        uow.commit()

    return cache_service.delete_by_email(email)
