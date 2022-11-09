import databases
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

DATABASE_URI = "postgresql+asyncpg://postgres:postgres@db:5432/test_db"
engine = create_engine(DATABASE_URI, connect_args={"check_same_thread": True})
database = databases.Database(DATABASE_URI)
Base = declarative_base()
