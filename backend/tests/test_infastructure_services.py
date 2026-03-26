import json
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import jwt
import pytest

from account.domain.entities import Account
from account.infrastructure.auth import JWTAuthService
from account.infrastructure.cache import redis_cache_service
from account.infrastructure.cache.redis_cache_service import RedisCacheService
from account.infrastructure.notifications import smtp_mail_sender
from account.infrastructure.notifications.smtp_mail_sender import (
    SMTPMailSender,
)
from account.infrastructure.security.bcrypt_password_service import (
    BcryptPasswordService,
)
from app.config import settings

JWT_SECRET = 'secret-key-for-tests-32-characters'


class TestJWTAuthService:
    def test_create_token_pair_returns_valid_access_and_refresh_tokens(
        self,
    ) -> None:
        service = JWTAuthService(JWT_SECRET, 'HS256')

        token_pair = service.create_token_pair(account_id=42)
        access_payload = jwt.decode(
            token_pair['access_token'],
            JWT_SECRET,
            algorithms=['HS256'],
        )
        refresh_payload = jwt.decode(
            token_pair['refresh_token'],
            JWT_SECRET,
            algorithms=['HS256'],
        )

        assert access_payload['sub'] == '42'
        assert access_payload['type'] == 'access'
        assert refresh_payload['sub'] == '42'
        assert refresh_payload['type'] == 'refresh'
        assert token_pair['token_type'] == 'Bearer'
        assert token_pair['expires_in'] == 900

    def test_refresh_token_pair_returns_new_pair(self) -> None:
        service = JWTAuthService(JWT_SECRET, 'HS256')
        refresh_token = service.create_token_pair(42)['refresh_token']

        refreshed_pair = service.refresh_token_pair(refresh_token)
        access_payload = jwt.decode(
            refreshed_pair['access_token'],
            JWT_SECRET,
            algorithms=['HS256'],
        )
        refresh_payload = jwt.decode(
            refreshed_pair['refresh_token'],
            JWT_SECRET,
            algorithms=['HS256'],
        )

        assert access_payload['sub'] == '42'
        assert access_payload['type'] == 'access'
        assert refresh_payload['sub'] == '42'
        assert refresh_payload['type'] == 'refresh'

    def test_refresh_token_pair_rejects_expired_token(self) -> None:
        service = JWTAuthService(JWT_SECRET, 'HS256')
        expired_refresh_token = jwt.encode(
            {
                'sub': '42',
                'type': 'refresh',
                'exp': datetime.now(timezone.utc) - timedelta(seconds=1),
            },
            JWT_SECRET,
            algorithm='HS256',
        )

        with pytest.raises(ValueError, match='refresh токен истек'):
            service.refresh_token_pair(expired_refresh_token)

    def test_refresh_token_pair_rejects_access_token(self) -> None:
        service = JWTAuthService(JWT_SECRET, 'HS256')
        access_token = service.create_token_pair(42)['access_token']

        with pytest.raises(ValueError, match='Не refresh токен'):
            service.refresh_token_pair(access_token)

    def test_get_payload_rejects_refresh_token(self) -> None:
        service = JWTAuthService(JWT_SECRET, 'HS256')
        refresh_token = service.create_token_pair(42)['refresh_token']

        with pytest.raises(ValueError, match='Не access токен'):
            service.get_payload(refresh_token)

    def test_get_payload_rejects_invalid_token(self) -> None:
        service = JWTAuthService(JWT_SECRET, 'HS256')

        with pytest.raises(ValueError, match='Невалидный токен'):
            service.get_payload('not-a-jwt')


class TestBcryptPasswordService:
    def test_hash_password_returns_hash(self) -> None:
        password_hash = BcryptPasswordService.hash_password('secret')

        assert password_hash != 'secret'
        assert isinstance(password_hash, str)

    def test_check_password_validates_hash(self) -> None:
        password_hash = BcryptPasswordService.hash_password('secret')

        assert BcryptPasswordService.check_password('secret', password_hash)
        assert not BcryptPasswordService.check_password(
            'wrong',
            password_hash,
        )


class TestRedisCacheService:
    def test_post_confirmation_code_stores_normalized_email_and_ttl(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        redis_client = MagicMock()
        redis_factory = MagicMock(return_value=redis_client)
        monkeypatch.setattr(redis_cache_service.redis, 'Redis', redis_factory)
        service = RedisCacheService()
        account = Account(
            id=1,
            email=' User@Example.com ',
            username='user',
            password_hash='hashed',
        )

        service.post_confirmation_code(account, 123456)

        redis_factory.assert_called_once_with(
            settings.redis_host,
            settings.redis_port,
            decode_responses=True,
        )
        redis_client.set.assert_called_once_with(
            'mail_confirmation:user@example.com',
            json.dumps(
                {
                    'username': 'user',
                    'password_hash': 'hashed',
                    'code': 123456,
                }
            ),
            ex=settings.code_expires_in,
        )

    def test_get_info_by_email_returns_deserialized_payload(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        redis_client = MagicMock()
        redis_client.get.return_value = json.dumps(
            {
                'username': 'user',
                'password_hash': 'hashed',
                'code': 123456,
            }
        )
        monkeypatch.setattr(
            redis_cache_service.redis,
            'Redis',
            MagicMock(return_value=redis_client),
        )
        service = RedisCacheService()

        payload = service.get_info_by_email(' User@Example.com ')

        assert payload == {
            'username': 'user',
            'password_hash': 'hashed',
            'code': 123456,
        }
        redis_client.get.assert_called_once_with(
            'mail_confirmation:user@example.com'
        )

    def test_get_info_by_email_returns_none_for_invalid_json(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        redis_client = MagicMock()
        redis_client.get.return_value = '{invalid-json'
        monkeypatch.setattr(
            redis_cache_service.redis,
            'Redis',
            MagicMock(return_value=redis_client),
        )
        service = RedisCacheService()

        payload = service.get_info_by_email('user@example.com')

        assert payload is None

    def test_delete_by_email_returns_bool_from_redis_delete(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        redis_client = MagicMock()
        redis_client.delete.return_value = 1
        monkeypatch.setattr(
            redis_cache_service.redis,
            'Redis',
            MagicMock(return_value=redis_client),
        )
        service = RedisCacheService()

        result = service.delete_by_email(' User@Example.com ')

        assert result is True
        redis_client.delete.assert_called_once_with(
            'mail_confirmation:user@example.com'
        )


class TestSMTPMailSender:
    def test_send_code_logs_in_and_sends_message(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        smtp_server = MagicMock()
        smtp_context_manager = MagicMock()
        smtp_context_manager.__enter__.return_value = smtp_server
        smtp_factory = MagicMock(return_value=smtp_context_manager)
        monkeypatch.setattr(
            smtp_mail_sender.smtplib,
            'SMTP_SSL',
            smtp_factory,
        )
        sender = SMTPMailSender()

        sender.send_code(123456, 'user@example.com')

        smtp_factory.assert_called_once_with(
            settings.smtp_host,
            settings.smtp_port,
            timeout=10,
        )
        smtp_server.login.assert_called_once_with(
            settings.email_login,
            settings.email_password,
        )
        smtp_server.send_message.assert_called_once()

        message = smtp_server.send_message.call_args.args[0]
        assert message['Subject'] == 'Подтверждение регистрации'
        assert message['From'] == settings.email_login
        assert message['To'] == 'user@example.com'
        assert message.get_payload(decode=True).decode('utf-8') == (
            'Ваш код подтверждения: 123456'
        )
