from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.models.users import User
from backend.models import habit_log as habit_log_models
from backend.models import habit as habit_models
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
    habit = db.query(habit_models.Habit).filter(
        habit_models.Habit.id == habit_log.habit_id,
        habit_models.Habit.user_id == current_user.id
    ).first()

    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found or unauthorized")

    new_log = habit_log_models.HabitLog(
        habit_id=habit_log.habit_id,
        status=habit_log.status or "done"
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
    logs = db.query(habit_log_models.HabitLog).join(habit_models.Habit).filter(
        habit_models.Habit.user_id == current_user.id
    ).all()
    return logs


# ✏️ Update a habit log entry
@router.put("/{log_id}", response_model=schemas.HabitLogOut)
def update_habit_log(
    log_id: int,
    habit_log_update: schemas.HabitLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user)
):
    # Find the habit log that belongs to the current user
    log = (
        db.query(habit_log_models.HabitLog)
        .join(habit_models.Habit)
        .filter(
            habit_log_models.HabitLog.id == log_id,
            habit_models.Habit.user_id == current_user.id
        )
        .first()
    )

    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit log not found or unauthorized"
        )

    # Only update fields if they are provided
    if habit_log_update.log_date is not None:
        log.log_date = habit_log_update.log_date

    if habit_log_update.status is not None:
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
    logs = db.query(habit_log_models.HabitLog).join(habit_models.Habit).filter(
        habit_models.Habit.id == habit_id,
        habit_models.Habit.user_id == current_user.id
    ).all()
    return logs


# ❌ Delete a habit log entry
@router.delete("/{log_id}")
def delete_habit_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user)
):
    log = db.query(habit_log_models.HabitLog).join(habit_models.Habit).filter(
        habit_log_models.HabitLog.id == log_id,
        habit_models.Habit.user_id == current_user.id
    ).first()

    if not log:
        raise HTTPException(status_code=404, detail="Habit log not found or unauthorized")

    db.delete(log)
    db.commit()
    return {"detail": "Habit log deleted successfully"}