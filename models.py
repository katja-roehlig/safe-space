from sqlalchemy import Boolean, Column, Integer, String
from database import Base


class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    content = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False)

    def __repr__(self):
        return f"Exercise: {self.id}: {self.title} in {self.category}"

    def __str__(self):
        return f"Exercise: {self.title}"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    mail = Column(String(100), nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    nickname = Column(String(50), nullable=False)
    is_admin = Column(Boolean, default=False)
