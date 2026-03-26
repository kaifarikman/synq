"""Ручки FastApi приложения в контексте Authentication(пока что)"""

from fastapi import APIRouter, Depends, HTTPException

from account.application.exceptions import (
    AccountAlreadyExist,
    AccountIsDeactivate,
    AccountNotFound,
    InvalidPassword,
)
from account.application.use_cases import AuthUseCases
from account.infrastructure.auth import JWTAuthService
from account.infrastructure.cache import RedisCacheService
from account.infrastructure.notifications import SMTPMailSender
from account.infrastructure.persistence.repositories import (
    SQLAlchemyAccountRepository,
)
from account.infrastructure.security import (
    BcryptPasswordService,
)
from app.api.schemas import AccountRegisterSchema, AccountLoginSchema, EmailConfirmation
from app.config import settings
from profile.infrastructure.persistence.repositories import (
    SQLAlchemyProfileRepository,
)

auth = APIRouter(prefix='/auth', tags=['auth'])


def get_auth_use_cases() -> AuthUseCases:
    return AuthUseCases(
        account_repository=SQLAlchemyAccountRepository(),
        password_service=BcryptPasswordService(),
        auth_service=JWTAuthService(settings.secret, settings.algorithm),
        mail_sender=SMTPMailSender(),
        cache_service=RedisCacheService(),
        profile_repository=SQLAlchemyProfileRepository(),
    )


@auth.post('/registry')
async def registry(
        account: AccountRegisterSchema, auth: AuthUseCases = Depends(get_auth_use_cases)
) -> bool:
    try:
        return auth.register(
            email=account.email,
            username=account.username,
            password=account.password,
        )
    except AccountAlreadyExist as err:
        raise HTTPException(status_code=409, detail=str(err)) from err


@auth.post('/confirm_email')
async def confirm_email(
        attempt: EmailConfirmation,
        auth: AuthUseCases = Depends(get_auth_use_cases),
) -> bool:
    try:
        res = auth.mail_confirmation(attempt.email, attempt.code)
        if not res:
            raise HTTPException(
                status_code=400, detail='Неверный код подтверждения'
            )
        return res
    except AccountAlreadyExist as err:
        raise HTTPException(status_code=409, detail=str(err)) from err


@auth.post('/login')
async def login(
        account: AccountLoginSchema, auth: AuthUseCases = Depends(get_auth_use_cases)
) -> dict:
    try:
        return auth.login(account.email, account.password)
    except AccountNotFound as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except InvalidPassword as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except AccountIsDeactivate as err:
        raise HTTPException(status_code=403, detail=str(err)) from err
