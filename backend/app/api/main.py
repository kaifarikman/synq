"""Отвечает за запуск FastAPI-приложения и подключение роутов"""

from fastapi import FastAPI

from app.api.auth_routes import auth

app = FastAPI(title='SYNQ')
app.include_router(auth)
