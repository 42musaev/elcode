from sqlalchemy import (
    Column,
    Integer,
    String,
)

from app.database.conf import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=256))
    surname = Column(String(length=256))
