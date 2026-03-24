"""Отвечает за технические сервисы контекста"""

import json
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from typing import Any, cast

import bcrypt
import jwt
import redis

from account.domain.entities import Account
from app.config import settings


class BcryptPasswordService:
    @staticmethod
    def hash_password(password: str) -> str:
        return (
            bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        ).decode()

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode('utf-8'), hashed_password.encode('utf-8')
        )


class JWTAuthService:
    def __init__(self, secret: str, algorithm: str) -> None:
        self.__secret = secret
        self.access_token_expire = timedelta(minutes=15)
        self.refresh_token_expire = timedelta(days=30)
        self.algorithm = algorithm

    def create_token_pair(self, account_id: int) -> dict:
        now = datetime.now(timezone.utc)
        access_payload = {
            'sub': str(account_id),
            'type': 'access',
            'exp': now + self.access_token_expire,
        }
        access_token = jwt.encode(
            access_payload, self.__secret, algorithm=self.algorithm
        )

        refresh_payload = {
            'sub': str(account_id),
            'type': 'refresh',
            'exp': now + self.refresh_token_expire,
        }
        refresh_token = jwt.encode(
            refresh_payload, self.__secret, algorithm=self.algorithm
        )

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': int(self.access_token_expire.total_seconds()),
        }

    def refresh_token_pair(self, refresh_token: str) -> dict:
        try:
            payload = jwt.decode(
                refresh_token, self.__secret, algorithms=[self.algorithm]
            )
            if payload.get('type') != 'refresh':
                raise ValueError('Не refresh токен')

            account_id = int(payload['sub'])
            return self.create_token_pair(account_id)
        except jwt.ExpiredSignatureError as err:
            raise ValueError('refresh токен истек') from err
        except jwt.InvalidTokenError as err:
            raise ValueError('Невалидный токен') from err

    def get_payload(self, access_token: str) -> dict:
        try:
            payload = jwt.decode(
                access_token, self.__secret, algorithms=[self.algorithm]
            )
            if payload.get('type') != 'access':
                raise ValueError('Не access токен')
            return payload
        except jwt.ExpiredSignatureError as err:
            raise ValueError('Токен истек') from err
        except jwt.InvalidTokenError as err:
            raise ValueError('Невалидный токен') from err


class SMTPMailSender:
    def send_code(self, code: int, to_email: str) -> None:
        subject = 'Подтверждение регистрации'
        body = f'Ваш код подтверждения: {code}'

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = settings.email_login
        msg['To'] = to_email

        with smtplib.SMTP_SSL(
            settings.smtp_host, settings.smtp_port, timeout=10
        ) as server:
            server.login(settings.email_login, settings.email_password)
            server.send_message(msg)


class RedisCacheService:
    def post_confirmation_code(self, account: Account, code: int) -> None:
        redis_client = redis.Redis(
            settings.redis_host, settings.redis_port, decode_responses=True
        )
        email = account.email.strip().lower()
        key = f'mail_confirmation:{email}'

        data: dict[str, Any] = {
            'username': account.username,
            'password_hash': account.password_hash,
            'code': code,
        }

        redis_client.set(
            key,
            json.dumps(data),
            ex=settings.code_expires_in,
        )

    def get_info_by_email(self, email: str) -> dict | None:
        redis_client = redis.Redis(
            settings.redis_host, settings.redis_port, decode_responses=True
        )
        email = email.strip().lower()
        key = f'mail_confirmation:{email}'
        data = redis_client.get(key)
        data = cast(str | bytes | None, data)
        if data is None:
            return None
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return None

    def delete_by_email(self, email: str) -> bool:
        redis_client = redis.Redis(
            settings.redis_host, settings.redis_port, decode_responses=True
        )
        email = email.strip().lower()
        key = f'mail_confirmation:{email}'
        return bool(redis_client.delete(key))
