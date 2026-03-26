from account.application.exceptions import (
    AccountHasNoId,
    AccountIsDeactivate,
    AccountNotFound,
    InvalidPassword,
)
from account.application.interfaces.auth_service import AuthService
from account.application.interfaces.password_service import PasswordService
from account.application.interfaces.uow import UnitOfWork


def login(
    uow: UnitOfWork,
    password_service: PasswordService,
    auth_service: AuthService,
    email: str,
    password: str,
) -> dict[str, str | int]:
    with uow:
        user = uow.accounts.get_by_email(email)

        if not user:
            raise AccountNotFound('Не существует аккаунта с таким email')

        if not user.can_login:
            raise AccountIsDeactivate('Аккаунт деактивирован')

        if not password_service.check_password(password, user.password_hash):
            raise InvalidPassword('Неверный email или пароль')

        if user.id is None:
            raise AccountHasNoId('У аккаунта нет id')

        return auth_service.create_token_pair(user.id)
