from sqlalchemy import select
from sqlalchemy.orm import Session

from account.domain.entities import Account
from account.infrastructure.persistence.mappers import AccountMapper
from account.infrastructure.persistence.models import UserModel


class SQLAlchemyAccountRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, account_id: int) -> Account | None:
        user = self.session.get(UserModel, account_id)
        return AccountMapper.to_domain(user) if user else None

    def get_by_email(self, email: str) -> Account | None:
        query = select(UserModel).where(UserModel.email == email)
        user = self.session.scalar(query)
        return AccountMapper.to_domain(user) if user else None

    def get_by_username(self, username: str) -> Account | None:
        query = select(UserModel).where(UserModel.username == username)
        user = self.session.scalar(query)
        return AccountMapper.to_domain(user) if user else None

    def save(self, account: Account) -> Account:
        user = (
            self.session.get(UserModel, account.id)
            if account.id is not None
            else None
        )

        if user:
            user.email = account.email
            user.username = account.username
            user.password_hash = account.password_hash
            user.is_active = account.is_active
        else:
            user = UserModel(
                email=account.email,
                username=account.username,
                password_hash=account.password_hash,
                is_active=account.is_active,
            )
            self.session.add(user)
            self.session.flush()

        return AccountMapper.to_domain(user)
