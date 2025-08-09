from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.models.users import User
from backend.models import habit as models
from backend.schemas import habit as schemas
from backend.utils import oauth2

router = APIRouter(prefix="/habits", tags=["Habits"])


@router.post("/", response_model=schemas.HabitOut)
def create_habit(
    habit: schemas.HabitCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    
    # Check if habit already exists for this user
    existing_habit = db.query(models.Habit).filter(
        models.Habit.user_id == current_user.id,
        models.Habit.goal_name == habit.goal_name
    ).first()

    if existing_habit:
        raise HTTPException(status_code=400, detail="You already have a habit with this name.")

    new_habit = models.Habit(
        goal_name=habit.goal_name,
        frequency=habit.frequency,
        start_date=habit.start_date,
        user_id=current_user.id,
    )
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return new_habit

# get all Habits
@router.get("/", response_model=list[schemas.HabitOut])
def get_habits(
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
):
    habits = db.query(models.Habit).filter(models.Habit.user_id == current_user.id).all()
    return habits
# get habits by ID

@router.get("/{habit_id}", response_model=schemas.HabitOut)
def get_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
):
    habit = (
        db.query(models.Habit)
        .filter(models.Habit.id == habit_id, models.Habit.user_id == current_user.id)
        .first()
    )
    if not habit:
        raise HTTPException (status_code=404, detail="Habit not found")
    return habit

@router.put("/{habit_id}", response_model=schemas.HabitOut)
def update_habit(
    habit_id: int,
    habit_data: schemas.HabitCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id, models.Habit.user_id == current_user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    habit.goal_name = habit_data.goal_name
    habit.frequency = habit_data.frequency
    habit.start_date = habit_data.start_date

    db.commit()
    db.refresh(habit)
    return habit


@router.delete("/{habit_id}")
def delete_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id, models.Habit.user_id == current_user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    db.delete(habit)
    db.commit()
    return {"message": "Habit deleted successfully"}
