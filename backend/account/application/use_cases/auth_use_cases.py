"""Сценарии использования Authentication"""

from account.application.read_models import CurrentUserReadModel
from account.domain.ports import (
    AccountRepository,
    AuthService,
    CacheService,
    MailSender,
    PasswordService,
)
from profile.domain.ports import ProfileRepository

from .confirm_email import confirm_email
from .get_current_user import get_current_user
from .login import login
from .logout import logout
from .register import register


class AuthUseCases:
    def __init__(
        self,
        account_repository: AccountRepository,
        password_service: PasswordService,
        auth_service: AuthService,
        mail_sender: MailSender,
        cache_service: CacheService,
        profile_repository: ProfileRepository,
    ):
        self.account_repository = account_repository
        self.password_service = password_service
        self.auth_service = auth_service
        self.mail_sender = mail_sender
        self.cache_service = cache_service
        self.profile_repository = profile_repository

    def register(self, email: str, username: str, password: str) -> bool:
        return register(
            account_repository=self.account_repository,
            password_service=self.password_service,
            mail_sender=self.mail_sender,
            cache_service=self.cache_service,
            email=email,
            username=username,
            password=password,
        )

    def login(self, email: str, password: str) -> dict:
        return login(
            account_repository=self.account_repository,
            password_service=self.password_service,
            auth_service=self.auth_service,
            email=email,
            password=password,
        )

    def mail_confirmation(self, email: str, enter_code: int) -> bool:
        return confirm_email(
            account_repository=self.account_repository,
            cache_service=self.cache_service,
            profile_repository=self.profile_repository,
            email=email,
            enter_code=enter_code,
        )

    def get_current_user(self, access_token: str) -> CurrentUserReadModel:
        return get_current_user(
            account_repository=self.account_repository,
            auth_service=self.auth_service,
            access_token=access_token,
        )

    def logout(self, access_token: str) -> None:
        logout(
            auth_service=self.auth_service,
            access_token=access_token,
        )
