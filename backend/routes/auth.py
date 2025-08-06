from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models import users as models # to -do 
from backend.schemas import user as schemas  # to -do 
from backend.database.connection import get_db # to -do 
from backend.utils.hashing import Hash # to -do 
# 
from fastapi.security import OAuth2PasswordRequestForm
from backend.utils.oauth2 import create_access_token

router = APIRouter()

@router.post("/register", response_model=schemas.ShowUser)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user_by_username = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user_by_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Check if email already exists
    existing_user_by_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=Hash.bcrypt(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user or not Hash.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}