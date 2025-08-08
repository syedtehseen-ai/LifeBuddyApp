from pydantic import BaseModel
from datetime import datetime


class HabitLogCreate(BaseModel):
    habit_id: int


class HabitLogOut(BaseModel):
    id: int
    habit_id: int
    completed_at: datetime

    class Config:
        orm_mode = True
