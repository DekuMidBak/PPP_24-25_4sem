from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut, UserMe
from app.cruds import user as user_crud
from app.core import security
from app.core.deps import get_db, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.token import TokenResponse

router = APIRouter()


@router.post("/sign-up/", response_model=UserOut)
def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = user_crud.create_user(db, user)
    token = security.create_access_token({"sub": new_user.email})
    return {"id": new_user.id, "email": new_user.email, "token": token}


@router.post("/login/", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, form_data.username)
    if not user or not user_crud.verify_password(form_data.password,
                                                 user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = security.create_access_token(user.email)
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/users/me/", response_model=UserMe)
def read_users_me(current_user=Depends(get_current_user)):
    return current_user
