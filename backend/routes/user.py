# Only authenticated users should access some routes.

from fastapi import APIRouter, Depends
from backend.utils.oauth2 import get_current_user
from backend import schemas

router = APIRouter()

@router.get("/profile", response_model=schemas.ShowUser)
def get_profile(current_user: schemas.user = Depends(get_current_user)):
    return current_user
