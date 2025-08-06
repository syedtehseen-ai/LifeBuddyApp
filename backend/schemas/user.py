from pydantic import BaseModel, EmailStr

# Schema for creating a new user
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Schema to show user response (exclude password)
class ShowUser(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
# backend/schemas/user.py

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


