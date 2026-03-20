from dataclasses import dataclass

"""Доменная модель внутри Authentication"""


@dataclass
class Account:
    id: int
    email: str
    password_hash: str
    is_active: bool

    @property
    def can_login(self) -> bool:
        return self.is_active

    @property
    def activate(self) -> None:
        self.is_active = True

    @property
    def deactivate(self) -> None:
        self.is_active = False
