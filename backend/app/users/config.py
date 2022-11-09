from dataclasses import dataclass


@dataclass
class Config:
    ACCESS_TOKEN_SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    REFRESH_TOKEN_SECRET_KEY: str = "09d22e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 40
    REFRESH_TOKEN_EXPIRE_DAYS: int = 15
