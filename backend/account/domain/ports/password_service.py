from typing import Protocol


class PasswordService(Protocol):
    @staticmethod
    def hash_password(password: str) -> str: ...

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool: ...
