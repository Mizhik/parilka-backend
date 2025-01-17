from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = "yourdbuser"
    POSTGRES_PASSWORD: str = "yourdbpassword"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_HOST_SYNC: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_LOCAL_PORT: int = 5432
    POSTGRES_DB: str = "yourdbname"

    PORT: int = 8000
    LOCAL_PORT: int = 8000
    HOST: str = "0.0.0.0"
    RELOAD: bool = True
    STR_ALLOWED_ORIGINS: str = "*,example.url"

    AUTH_SECRET_KEY: str = "your_secret_key"
    AUTH_ALGORITHM: str = "algorithm"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST_SYNC}:{self.POSTGRES_LOCAL_PORT}/{self.POSTGRES_DB}"

    @property
    def ALLOWED_ORIGINS_LIST(self) -> list:
        return self.STR_ALLOWED_ORIGINS.split(",")

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )


config = Settings()
