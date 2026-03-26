from profile.domain.ports.profile_repository import ProfileRepository
from profile.infrastructure.persistence.repositories.sqlalchemy_profile_repository import (  # noqa: E501
    SQLAlchemyProfileRepository,
)
from types import TracebackType
from typing import Optional, Self, Type

from account.domain.ports.account_repository import AccountRepository
from account.infrastructure.persistence.repositories.sqlalchemy_account_repository import (  # noqa: E501
    SQLAlchemyAccountRepository,
)
from app.db import Session


class SqlAlchemyUnitOfWork:
    accounts: AccountRepository
    profiles: ProfileRepository

    def __init__(self) -> None:
        self.session = Session()
        self.accounts: AccountRepository = SQLAlchemyAccountRepository(
            self.session
        )
        self.profiles: ProfileRepository = SQLAlchemyProfileRepository(
            self.session
        )

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if exc_type is not None:
            self.rollback()
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
