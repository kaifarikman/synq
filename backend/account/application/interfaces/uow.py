from profile.domain.ports.profile_repository import ProfileRepository
from types import TracebackType
from typing import Optional, Protocol, Self, Type

from account.domain.ports.account_repository import AccountRepository


class UnitOfWork(Protocol):
    accounts: AccountRepository
    profiles: ProfileRepository

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None: ...

    def commit(self) -> None: ...
    def rollback(self) -> None: ...
