from profile.domain.entities import Profile
from profile.infrastructure.persistence.models import ProfileModel
from profile.infrastructure.persistence.repositories.sqlalchemy_profile_repository import (  # noqa: E501
    SQLAlchemyProfileRepository,
)
from uuid import UUID

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from account.domain.entities import Account
from account.infrastructure.persistence.models import UserModel
from account.infrastructure.persistence.repositories.sqlalchemy_account_repository import (  # noqa: E501
    SQLAlchemyAccountRepository,
)
from account.infrastructure.uow import sqlalchemy_uow
from account.infrastructure.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork
from app.db import Base


@pytest.fixture()
def engine():
    engine = create_engine('sqlite+pysqlite:///:memory:')
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture()
def session_factory(engine):
    return sessionmaker(bind=engine)


@pytest.fixture()
def db_session(session_factory):
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


class TestSQLAlchemyAccountRepository:
    def test_save_creates_account_and_supports_all_lookups(
        self,
        session_factory,
        db_session,
    ) -> None:
        repo = SQLAlchemyAccountRepository(db_session)

        saved_account = repo.save(
            Account(
                email='user@example.com',
                username='user',
                password_hash='hashed',
                is_active=True,
            )
        )
        db_session.commit()

        with session_factory() as verification_session:
            verification_repo = SQLAlchemyAccountRepository(
                verification_session
            )
            by_id = verification_repo.get_by_id(saved_account.id)
            by_email = verification_repo.get_by_email('user@example.com')
            by_username = verification_repo.get_by_username('user')

        assert saved_account.id is not None
        assert by_id is not None
        assert by_email is not None
        assert by_username is not None
        assert by_id.email == 'user@example.com'
        assert by_email.username == 'user'
        assert by_username.password_hash == 'hashed'

    def test_save_updates_existing_account(
        self,
        session_factory,
        db_session,
    ) -> None:
        repo = SQLAlchemyAccountRepository(db_session)
        created_account = repo.save(
            Account(
                email='user@example.com',
                username='user',
                password_hash='hashed',
                is_active=True,
            )
        )
        db_session.commit()

        updated_account = repo.save(
            Account(
                id=created_account.id,
                email='updated@example.com',
                username='updated-user',
                password_hash='updated-hash',
                is_active=False,
            )
        )
        db_session.commit()

        with session_factory() as verification_session:
            verification_repo = SQLAlchemyAccountRepository(
                verification_session
            )
            persisted_account = verification_repo.get_by_id(created_account.id)

        assert updated_account.id == created_account.id
        assert persisted_account is not None
        assert persisted_account.email == 'updated@example.com'
        assert persisted_account.username == 'updated-user'
        assert persisted_account.password_hash == 'updated-hash'
        assert persisted_account.is_active is False


class TestSQLAlchemyProfileRepository:
    def test_save_creates_profile_and_gets_it_by_user_id(
        self,
        session_factory,
        db_session,
    ) -> None:
        account_repo = SQLAlchemyAccountRepository(db_session)
        profile_repo = SQLAlchemyProfileRepository(db_session)
        account = account_repo.save(
            Account(
                email='user@example.com',
                username='user',
                password_hash='hashed',
            )
        )
        db_session.commit()

        saved_profile = profile_repo.save(Profile(user_id=account.id))
        db_session.commit()

        with session_factory() as verification_session:
            verification_repo = SQLAlchemyProfileRepository(
                verification_session
            )
            by_id = verification_repo.get_by_id(saved_profile.id)
            by_user_id = verification_repo.get_by_user_id(account.id)

        assert saved_profile.id is not None
        assert isinstance(saved_profile.uuid, UUID)
        assert by_id is not None
        assert by_user_id is not None
        assert by_id.user_id == account.id
        assert by_user_id.id == saved_profile.id

    def test_save_updates_existing_profile(
        self,
        session_factory,
        db_session,
    ) -> None:
        account_repo = SQLAlchemyAccountRepository(db_session)
        profile_repo = SQLAlchemyProfileRepository(db_session)
        account = account_repo.save(
            Account(
                email='user@example.com',
                username='user',
                password_hash='hashed',
            )
        )
        profile = profile_repo.save(Profile(user_id=account.id))
        db_session.commit()

        updated_profile = profile_repo.save(
            Profile(
                id=profile.id,
                user_id=account.id,
                uuid=profile.uuid,
                full_name='Kai Farikman',
                bio='Integration test bio',
                created_at=profile.created_at,
                updated_at=profile.updated_at,
            )
        )
        db_session.commit()

        with session_factory() as verification_session:
            verification_repo = SQLAlchemyProfileRepository(
                verification_session
            )
            persisted_profile = verification_repo.get_by_id(profile.id)

        assert updated_profile.id == profile.id
        assert persisted_profile is not None
        assert persisted_profile.user_id == account.id
        assert persisted_profile.uuid == profile.uuid
        assert persisted_profile.full_name == 'Kai Farikman'
        assert persisted_profile.bio == 'Integration test bio'


class TestSqlAlchemyUnitOfWork:
    def test_commit_persists_changes(
        self,
        monkeypatch,
        session_factory,
    ) -> None:
        monkeypatch.setattr(sqlalchemy_uow, 'Session', session_factory)

        with SqlAlchemyUnitOfWork() as uow:
            saved_account = uow.accounts.save(
                Account(
                    email='user@example.com',
                    username='user',
                    password_hash='hashed',
                )
            )
            uow.commit()

        with session_factory() as verification_session:
            persisted_user = verification_session.get(
                UserModel,
                saved_account.id,
            )

        assert persisted_user is not None
        assert persisted_user.email == 'user@example.com'

    def test_rollback_on_exception_discards_changes(
        self,
        monkeypatch,
        session_factory,
    ) -> None:
        monkeypatch.setattr(sqlalchemy_uow, 'Session', session_factory)

        with pytest.raises(RuntimeError, match='boom'):
            with SqlAlchemyUnitOfWork() as uow:
                uow.accounts.save(
                    Account(
                        email='user@example.com',
                        username='user',
                        password_hash='hashed',
                    )
                )
                raise RuntimeError('boom')

        with session_factory() as verification_session:
            persisted_user = verification_session.get(UserModel, 1)

        assert persisted_user is None

    def test_commit_persists_profile_changes(
        self,
        monkeypatch,
        session_factory,
    ) -> None:
        monkeypatch.setattr(sqlalchemy_uow, 'Session', session_factory)

        with SqlAlchemyUnitOfWork() as uow:
            account = uow.accounts.save(
                Account(
                    email='user@example.com',
                    username='user',
                    password_hash='hashed',
                )
            )
            saved_profile = uow.profiles.save(
                Profile(
                    user_id=account.id,
                    full_name='Kai',
                    bio='Profile from uow',
                )
            )
            uow.commit()

        with session_factory() as verification_session:
            persisted_profile = verification_session.get(
                ProfileModel,
                saved_profile.id,
            )

        assert persisted_profile is not None
        assert persisted_profile.user_id == account.id
        assert persisted_profile.full_name == 'Kai'
        assert persisted_profile.bio == 'Profile from uow'
