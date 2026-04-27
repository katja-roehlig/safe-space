from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text, String
from app.core.database import Base
from sqlalchemy.orm import relationship


class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False, unique=True)
    instructions = Column(Text)
    media = Column(String, unique=True)

    def __repr__(self):
        return f"Exercise: {self.id}: {self.title} with {self.content} and instructions {self.instructions}"

    def __str__(self):
        return f"Exercise: {self.title}"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    mail = Column(String(100), nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    nickname = Column(String(50), nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)
    is_admin = Column(Boolean, default=False)
    properties = relationship("UserProperty", back_populates="user")


class UserProperty(Base):
    __tablename__ = "user_properties"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    user = relationship("User", back_populates="properties")

    def __repr__(self):
        return f"<UserProperty(id={self.id}, category='{self.category}',content ='{self.content}' active={self.is_active})>"
