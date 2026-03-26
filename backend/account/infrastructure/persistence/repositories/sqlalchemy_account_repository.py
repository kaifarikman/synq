from typing import Optional

from sqlalchemy import select

from account.domain.entities import Account
from account.infrastructure.persistence.mappers import AccountMapper
from account.infrastructure.persistence.models import UserModel
from app.db import Session


class SQLAlchemyAccountRepository:
    def get_by_id(self, account_id: int) -> Optional[Account]:
        with Session() as session:
            user = session.get(UserModel, account_id)
            return AccountMapper.to_domain(user) if user else None

    def get_by_email(self, email: str) -> Optional[Account]:
        with Session() as session:
            query = select(UserModel).where(UserModel.email == email)
            user = session.scalar(query)
            return AccountMapper.to_domain(user) if user else None

    def save(self, account: Account) -> Account:
        with Session() as session:
            user = session.get(UserModel, account.id)
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
                session.add(user)
            session.commit()
            session.refresh(user)
            return AccountMapper.to_domain(user)
