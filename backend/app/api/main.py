"""Отвечает за запуск FastAPI-приложения и подключение роутов"""

from fastapi import FastAPI

import app.db_registry
from app.api.auth_routes import auth
from app.config import settings

app = FastAPI(title='SYNQ')
app.include_router(auth, prefix=settings.api_prefix)
