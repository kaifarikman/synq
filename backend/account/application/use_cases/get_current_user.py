from account.application.exceptions import AccountNotFound
from account.domain.entities import Account
from account.domain.ports import AccountRepository, AuthService


def get_current_user(
    account_repository: AccountRepository,
    auth_service: AuthService,
    access_token: str,
) -> Account:
    payload = auth_service.get_payload(access_token)
    account_id = int(payload['sub'])
    account = account_repository.get_by_id(account_id)
    if account is None:
        raise AccountNotFound('Пользователь не найден')
    return account
