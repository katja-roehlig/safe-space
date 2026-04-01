from sqlalchemy import Column, Integer, String
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
