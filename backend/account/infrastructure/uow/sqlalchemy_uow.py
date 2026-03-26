from app.db import Session
from account.application.interfaces.uow import UnitOfWork
from account.infrastructure.persistence.repositories.sqlalchemy_account_repository import SQLAlchemyAccountRepository


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.session = Session()
        self.accounts = SQLAlchemyAccountRepository(self.session)

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.rollback()
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
