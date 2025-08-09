from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.base import Base
from typing import Optional
from datetime import datetime


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, nullable=False, default="pending")  # e.g., "done" or "missed"

    habit = relationship("Habit", back_populates="logs")

