from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class HabitLogCreate(BaseModel):
    habit_id: int
    status: Optional[str] = "pending"
    
class HabitLogUpdate(BaseModel):
    log_date: Optional[datetime]
    status: Optional[str]

class HabitLogOut(BaseModel):
    id: int
    habit_id: int
    #completed_at: datetime

    class Config:
        orm_mode = True
