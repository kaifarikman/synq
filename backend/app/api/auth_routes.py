"""Ручки FastApi приложения в контексте Authentication(пока что)"""

from fastapi import APIRouter, Depends, HTTPException

from account.application.exceptions import (
    AccountAlreadyExist,
    AccountIsDeactivate,
    AccountNotFound,
    InvalidPassword,
)
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

auth = APIRouter(prefix='/auth', tags=['auth'])


def get_auth_use_cases() -> AuthUseCases:
    return AuthUseCases(
        account_repository=SQLAlchemyAccountRepository(),
        password_service=BcryptPasswordService(),
        auth_service=JWTAuthService(settings.secret, settings.algorithm),
    )


@auth.post('/registry')
async def registry(
    account: AccountSchema, auth: AuthUseCases = Depends(get_auth_use_cases)
) -> Account:
    try:
        res_account = auth.resigtry(
            email=account.email, password=account.password
        )
        return res_account
    except AccountAlreadyExist as err:
        raise HTTPException(status_code=409, detail=str(err)) from err


@auth.post('/login')
async def login(
    account: AccountSchema, auth: AuthUseCases = Depends(get_auth_use_cases)
) -> dict:
    try:
        return auth.login(account.email, account.password)
    except AccountNotFound as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except InvalidPassword as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except AccountIsDeactivate as err:
        raise HTTPException(status_code=403, detail=str(err)) from err
