from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://root:letmeinnow@localhost:5432/weavr_db"
    TEST_DATABASE_URL: str = "sqlite+aiosqlite:///./test_weavr.db"

    class Config:
        env_file = ".env"


settings = Settings()

__all__ = ["BaseSettings", "Settings", "settings"]
