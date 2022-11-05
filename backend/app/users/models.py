from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean
)

from app.database.conf import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=256))
    hashed_password = Column(String(length=256))
    disable = Column(Boolean, default=False)
