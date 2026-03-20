"""Абстракция репозитория"""

from typing import Optional, Protocol

from .entities import Account


class AccountRepository(Protocol):
    def get_by_id(self, id: int) -> Optional[Account]: ...
    def get_by_email(self, email: str) -> Optional[Account]: ...
    def save(self, account: Account) -> None: ...


class PasswordService(Protocol):
    @staticmethod
    def hash_password(password: str) -> str: ...
    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool: ...
