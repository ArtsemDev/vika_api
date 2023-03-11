from sqlalchemy import Column, VARCHAR

from .base import Base


class Category(Base):
    name = Column(VARCHAR(64), nullable=False, unique=True)
    slug = Column(VARCHAR(64), nullable=False, unique=True)

    def __repr__(self) -> str:
        return self.name


class User(Base):
    email = Column(VARCHAR(128), nullable=False, unique=True)
    username = Column(VARCHAR(128), nullable=False)
    hashed_password = Column(VARCHAR(512), nullable=False)

    def __repr__(self) -> str:
        return self.email
