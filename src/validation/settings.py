from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, SecretStr, PositiveInt


class Settings(BaseSettings):
    DB_URL: PostgresDsn = "postgresql://blog:blog@127.0.0.1:5432/blog"
    SECRET_KEY: SecretStr = "super-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt = 500
    ALGORITHM: str = "HS256"


settings = Settings()

