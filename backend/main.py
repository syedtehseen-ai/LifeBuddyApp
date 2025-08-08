from fastapi import FastAPI
from dotenv import load_dotenv
from backend.database.connection import engine
from backend.models.users import User
from backend.database.base import Base
# importing the auth file here
from backend.routes import auth, user, habit, habit_log

load_dotenv()

backend = FastAPI(title="LifeBuddy backend", version="1.0.0")
# including the router
backend.include_router(auth.router, tags=["Auth"])
backend.include_router(user.router, prefix="/users", tags=["User"])
backend.include_router(habit.router, tags=["Habits"])
backend.include_router(habit_log.router, tags=["Habit_Logs"])


@backend.on_event("startup")
def startup():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created.")


@backend.get("/")
def root():
    return {"message": "Welcome to LifeBuddy!"}