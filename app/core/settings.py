from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    RELOAD: bool = True
    STR_ALLOWED_ORIGINS: str = "*,example.url"

    @property
    def ALLOWED_ORIGINS_LIST(self) -> list:
        return self.STR_ALLOWED_ORIGINS.split(",")

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )


config = Settings()
