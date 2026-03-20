"""Отвечает за ORM-модель для базы данных"""

from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    username: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, default=''
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_superuser: Mapped[bool] = mapped_column(nullable=False, default=False)

    # profile: Mapped[Any] = relationship(
    #     'Profile', back_populates='user', uselist=False
    # )
