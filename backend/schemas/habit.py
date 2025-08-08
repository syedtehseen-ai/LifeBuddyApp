# backend/schemas/habit.py

from pydantic import BaseModel, validator
from typing import Optional
from datetime import date, datetime

ALLOWED_FREQUENCIES = {"daily", "weekly", "monthly"}

class HabitCreate(BaseModel):
    goal_name: str
    frequency: str
    start_date: date
    

    # @validator("goal_name")
    # def validate_frequency(cls, value):
    #     if value not in ALLOWED_FREQUENCIES:
    #         raise ValueError("Name your goal")
    #     return value
    
    @validator("frequency")
    def validate_frequency(cls, value):
        if value not in ALLOWED_FREQUENCIES:
            raise ValueError("Frequency must be one of: daily, weekly, monthly")
        return value

    @validator("start_date")
    def validate_start_date(cls, value):
        if value < date.today():
            raise ValueError("Start date cannot be in the past")
        return value

class HabitOut(HabitCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
