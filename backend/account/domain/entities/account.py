from dataclasses import dataclass, field
from typing import Optional

"""Доменная модель внутри Authentication"""


@dataclass
class Account:
    email: str = field()
    username: str = field()
    password_hash: str = field()
    is_active: bool = field(default=True)
    id: Optional[int] = None

    @property
    def can_login(self) -> bool:
        return self.is_active

    @property
    def activate(self) -> None:
        self.is_active = True

    @property
    def deactivate(self) -> None:
        self.is_active = False
