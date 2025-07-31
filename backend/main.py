from fastapi import FastAPI
from dotenv import load_dotenv
from backend.database.connection import engine
from backend.models.users import User
from backend.database.base import Base
load_dotenv()
backend = FastAPI(title="LifeBuddy backend", version="1.0.0")


@backend.on_event("startup")
def startup():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created.")


@backend.get("/")
def root():
    return {"message": "Welcome to LifeBuddy!"}