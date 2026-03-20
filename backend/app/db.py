"""Подключение к базе данных"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

engine = create_engine(settings.database_url)

Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    __abstract__ = True
