"""Отвечает за технические сервисы контекста"""

import bcrypt


class BcryptPasswordService:
    @staticmethod
    def hash_password(password: str) -> str:
        return (
            bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        ).decode()

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode('utf-8'), hashed_password.encode('utf-8')
        )


class JWTService:
    pass
