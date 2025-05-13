from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str = "yourdbuser"
    POSTGRES_PASSWORD: str = "yourdbpassword"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_HOST_SYNC: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_LOCAL_PORT: int = 5432
    POSTGRES_DB: str = "yourdbname"
    POSTGRES_TEST_DB: str = "test_db"

    PORT: int = 8000
    LOCAL_PORT: int = 8000
    HOST: str = "0.0.0.0"
    RELOAD: bool = True
    STR_ALLOWED_ORIGINS: str = "*,example.url"

    AUTH_SECRET_KEY: str = "your_secret_key"
    AUTH_ALGORITHM: str = "algorithm"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DOCS_USER: str = "user"
    DOCS_PASSWORD: str = "password"

    REDIS_LOCAL_PORT: int = 6379
    REDIS_HOST: str = "redis"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_LOCAL_PORT}/{self.POSTGRES_DB}"

    @property
    def ASYNC_TEST_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost:{self.POSTGRES_PORT}/{self.POSTGRES_TEST_DB}"

    @property
    def SYNC_TEST_DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost:{self.POSTGRES_PORT}/{self.POSTGRES_TEST_DB}"

    @property
    def ALLOWED_ORIGINS_LIST(self) -> list:
        return self.STR_ALLOWED_ORIGINS.split(",")

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_LOCAL_PORT}"

    model_config = SettingsConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )


config = Settings()
