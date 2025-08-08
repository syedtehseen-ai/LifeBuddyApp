from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.models.users import User
from backend.models import habit_log as models
from backend.schemas import habit_log as schemas
from typing import List
from backend.utils import oauth2

router = APIRouter(prefix="/habit-logs",tags=["Habit Logs"])

# 🚀 Create Habit Log
@router.post("/", response_model=schemas.HabitLogOut)
def create_habit_log(
    habit_log: schemas.HabitLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user)
):
    # Check habit ownership
    habit = db.query(models.Habit).filter(
        models.Habit.id == habit_log.habit_id,
        models.Habit.user_id == current_user.id
    ).first()

    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found or unauthorized")

    new_log = models.HabitLog(
        habit_id=habit_log.habit_id,
        log_date=habit_log.log_date,
        status=habit_log.status
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log


# 📄 Get all logs for current user
@router.get("/", response_model=List[schemas.HabitLogOut])
def get_habit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user)
):
    logs = db.query(models.HabitLog).join(models.Habit).filter(
        models.Habit.user_id == current_user.id
    ).all()
    return logs


# ✏️ Update a habit log entry
@router.put("/{log_id}", response_model=schemas.HabitLogOut)
def update_habit_log(
    log_id: int,
    habit_log_update: schemas.HabitLogCreate,  # We can also make a separate HabitLogUpdate schema if needed
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user)
):
    log = db.query(models.HabitLog).join(models.Habit).filter(
        models.HabitLog.id == log_id,
        models.Habit.user_id == current_user.id
    ).first()

    if not log:
        raise HTTPException(status_code=404, detail="Habit log not found or unauthorized")

    log.log_date = habit_log_update.log_date
    log.status = habit_log_update.status

    db.commit()
    db.refresh(log)
    return log


# 🔍 Get logs for a specific habit
@router.get("/habit/{habit_id}", response_model=List[schemas.HabitLogOut])
def get_logs_for_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user)
):
    logs = db.query(models.HabitLog).join(models.Habit).filter(
        models.Habit.id == habit_id,
        models.Habit.user_id == current_user.id
    ).all()
    return logs


# ❌ Delete a habit log entry
@router.delete("/{log_id}")
def delete_habit_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user)
):
    log = db.query(models.HabitLog).join(models.Habit).filter(
        models.HabitLog.id == log_id,
        models.Habit.user_id == current_user.id
    ).first()

    if not log:
        raise HTTPException(status_code=404, detail="Habit log not found or unauthorized")

    db.delete(log)
    db.commit()
    return {"detail": "Habit log deleted successfully"}
