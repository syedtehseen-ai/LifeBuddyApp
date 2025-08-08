# backend/models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    habits = relationship("Habit", back_populates="user", cascade="all, delete-orphan")
