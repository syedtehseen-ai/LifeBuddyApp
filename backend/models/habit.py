# models/habit.py

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database.base import Base


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    goal_name = Column(String, index=True, nullable=False)
    frequency = Column(String, nullable=False)  # Can be 'daily', 'weekly', etc.
    start_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="habits")

    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")
# same user can’t create two habits with the same goal_name
    __table_args__ = (
        UniqueConstraint("user_id", "goal_name", name="uq_user_goalname"),
    )