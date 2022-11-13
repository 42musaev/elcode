import databases

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from app.config import get_settings

Base = declarative_base()
settings = get_settings()

DATABASE_URI = settings.get_database_url()
database = databases.Database(DATABASE_URI)
metadata = MetaData()
engine = create_engine(DATABASE_URI)
