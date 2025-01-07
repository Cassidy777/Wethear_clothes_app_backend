from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.models import User
from app.database import get_db
from app.utils.hashing import get_password_hash, verify_password
from pydantic import BaseModel

router = APIRouter()

@router.post("/register")
def register_user(username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    print(f"username: {username}, email: {email}, password: {password}")
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        print("Username already exists")
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print("User registered successfully")
    return {"message": "User registered successfully"}


class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful", "user_id": user.id}

