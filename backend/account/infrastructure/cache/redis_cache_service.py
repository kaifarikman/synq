import json
from typing import Any, cast

import redis

from account.domain.entities import Account
from app.config import settings


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
