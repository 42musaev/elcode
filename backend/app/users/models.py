from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    TIMESTAMP
)

from app.database.conf import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=256), nullable=False, unique=True)
    hashed_password = Column(String(length=512), nullable=False)
    refresh_token = Column(String(length=512), nullable=True)
    expires_token = Column(TIMESTAMP, nullable=True)
    disable = Column(Boolean, server_default=str(False).lower())
