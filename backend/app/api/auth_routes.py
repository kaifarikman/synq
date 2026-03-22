"""Ручки FastApi приложения в контексте Authentication(пока что)"""

from fastapi import APIRouter, Depends

from account.application.use_cases import AuthUseCases
from account.domain.entities import Account
from account.infrastructure.services import (
    BcryptPasswordService,
    JWTAuthService,
)
from account.infrastructure.sqlalchemy_repository import (
    SQLAlchemyAccountRepository,
)
from app.api.schemas import AccountSchema
from app.config import settings

auth = APIRouter(tags=['auth'])


def get_auth_use_cases() -> AuthUseCases:
    return AuthUseCases(
        account_repository=SQLAlchemyAccountRepository(),
        password_service=BcryptPasswordService(),
        auth_service=JWTAuthService(settings.secret, settings.algorithm),
    )


@auth.post('')
async def registry(
    account: AccountSchema, auth: AuthUseCases = Depends(get_auth_use_cases)
) -> Account:
    return auth.resigtry(email=account.email, password=account.password)
