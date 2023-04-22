import databases

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from app.config import settings

Base = declarative_base()

DATABASE_URI = settings.database_url
database = databases.Database(DATABASE_URI)
metadata = MetaData()
engine = create_engine(DATABASE_URI)
