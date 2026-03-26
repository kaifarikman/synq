from account.application.exceptions import AccountNotFound
from account.application.read_models import CurrentUserReadModel
from account.application.interfaces import AuthService
from account.application.interfaces.uow import UnitOfWork


def get_current_user(
    uow: UnitOfWork,
    auth_service: AuthService,
    access_token: str,
) -> CurrentUserReadModel:
    payload = auth_service.get_payload(access_token)
    account_id = int(payload["sub"])

    with uow:
        account = uow.accounts.get_by_id(account_id)

        if account is None or account.id is None:
            raise AccountNotFound("Пользователь не найден")

        return CurrentUserReadModel(
            id=account.id,
            email=account.email,
            username=account.username,
        )