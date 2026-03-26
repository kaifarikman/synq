"""Абстракция репозитория"""

from typing import Optional, Protocol

from account.domain.entities import Account


class AccountRepository(Protocol):
    def get_by_id(self, id: int) -> Optional[Account]: ...
    def get_by_email(self, email: str) -> Optional[Account]: ...
    def save(self, account: Account) -> Account: ...
