from account.domain.entities import Account
from account.infrastructure.persistence.models import UserModel


class AccountMapper:
    @staticmethod
    def to_domain(user: UserModel) -> Account:
        return Account(
            id=user.id,
            email=user.email,
            username=user.username,
            password_hash=user.password_hash,
            is_active=user.is_active,
        )
