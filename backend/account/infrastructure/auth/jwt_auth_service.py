from datetime import datetime, timedelta, timezone

import jwt


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
