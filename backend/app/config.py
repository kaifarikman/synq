"""Точка входа для настроек; доступна вся конфигурация"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_port: int
    secret: str
    algorithm: str
    base_url: str
    email_login: str
    email_password: str
    smtp_host: str
    smtp_port: int
    code_expires_in: int
    redis_host: str
    redis_port: int

    @property
    def database_url(self) -> str:
        return (
            f'postgresql+psycopg2://{self.db_user}:'
            f'{self.db_password}@localhost:{self.db_port}/{self.db_name}'
        )

    class Config:
        env_file = '.env'


settings = Settings()  # type: ignore[call-arg]
