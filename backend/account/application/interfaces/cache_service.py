from typing import Protocol

from account.domain.entities import Account


class CacheService(Protocol):
    def post_confirmation_code(self, account: Account, code: int) -> None: ...

    def get_info_by_email(self, email: str) -> dict | None: ...

    def delete_by_email(self, email: str) -> bool: ...
