"""Абстракция репозитория"""

from typing import Protocol

from .entities import Account


class AccountRepositoryProtocol(Protocol):
    def get_account_by_id(self, id: int) -> Account | None: ...
    def get_account_by_email(self, email: str) -> Account | None: ...
    def add_account(self, account: Account) -> None: ...
