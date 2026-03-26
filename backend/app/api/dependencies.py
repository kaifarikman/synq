"""Отвечает за общие зависимости FastAPI
Здесь лежит: get_db, получение репозиториев, получение сервисов"""

from profile.application.use_cases.profile_use_cases import ProfileUseCases

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from account.application.use_cases import AuthUseCases
from account.infrastructure.auth import JWTAuthService
from account.infrastructure.cache import RedisCacheService
from account.infrastructure.notifications import SMTPMailSender
from account.infrastructure.security import (
    BcryptPasswordService,
)
from account.infrastructure.uow.sqlalchemy_uow import (
    SqlAlchemyUnitOfWork as account_uow,
)
from app.config import settings

bearer_scheme = HTTPBearer(auto_error=False)


def get_profile_use_cases() -> ProfileUseCases:
    return ProfileUseCases(
        uow=account_uow(),
    )


def get_auth_use_cases() -> AuthUseCases:
    return AuthUseCases(
        uow=account_uow(),
        password_service=BcryptPasswordService(),
        auth_service=JWTAuthService(settings.secret, settings.algorithm),
        mail_sender=SMTPMailSender(),
        cache_service=RedisCacheService(),
    )


def get_bearer_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    if credentials is None or credentials.scheme.lower() != 'bearer':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен отсутствует или недействителен',
        )
    return credentials.credentials
