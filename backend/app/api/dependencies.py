"""Отвечает за общие зависимости FastAPI
Здесь лежит: get_db, получение репозиториев, получение сервисов"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from account.application.use_cases import AuthUseCases
from account.infrastructure.auth import JWTAuthService
from account.infrastructure.cache import RedisCacheService
from account.infrastructure.notifications import SMTPMailSender
from account.infrastructure.security import (
    BcryptPasswordService,
)
from account.infrastructure.persistence.repositories import SQLAlchemyAccountRepository
from profile.infrastructure.persistence.repositories import SQLAlchemyProfileRepository
from app.config import settings

bearer_scheme = HTTPBearer(auto_error=False)

def get_auth_use_cases() -> AuthUseCases:
    return AuthUseCases(
        account_repository=SQLAlchemyAccountRepository(),
        password_service=BcryptPasswordService(),
        auth_service=JWTAuthService(settings.secret, settings.algorithm),
        mail_sender=SMTPMailSender(),
        cache_service=RedisCacheService(),
        profile_repository=SQLAlchemyProfileRepository(),
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
