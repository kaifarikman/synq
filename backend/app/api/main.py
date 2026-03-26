"""Отвечает за запуск FastAPI-приложения и подключение роутов"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.db_registry
from app.api.auth_routes import auth
from app.api.profile_routes import profile
from app.config import settings

app = FastAPI(title='SYNQ')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://127.0.0.1:5173',
        'http://localhost:5173',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(auth, prefix=settings.api_prefix)
app.include_router(profile, prefix=settings.api_prefix)
