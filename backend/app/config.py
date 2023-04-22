# from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    ACCESS_TOKEN_SECRET_KEY: str
    REFRESH_TOKEN_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 40
    REFRESH_TOKEN_EXPIRE_DAYS: int = 15

    TESTING: bool
    DATABASE_URL: str
    DATABASE_TEST_URL: str

    @property
    def database_url(self):
        if self.TESTING:
            return self.DATABASE_TEST_URL
        return self.DATABASE_URL

    class Config:
        env_file = "app/.env"


settings = Settings()
