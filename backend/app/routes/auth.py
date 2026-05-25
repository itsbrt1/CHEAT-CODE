from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import (
    SessionLocal,
    engine
)

from app.models import (
    User,
    Base
)

from passlib.context import CryptContext



Base.metadata.create_all(bind=engine)

router = APIRouter()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)



class UserCreate(BaseModel):

    username: str

    password: str




@router.post("/signup")

def signup(user: UserCreate):

    db: Session = SessionLocal()

    username = user.username.strip()

    password = user.password.strip()



    if username == "":

        raise HTTPException(
            status_code=400,
            detail="Username required"
        )



    if password == "":

        raise HTTPException(
            status_code=400,
            detail="Password required"
        )



    # LIMIT PASSWORD SIZE

    password = password[:50]



    existing = db.query(User).filter(
        User.username == username
    ).first()



    if existing:

        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )



    hashed_password = pwd_context.hash(
        password
    )



    new_user = User(
        username=username,
        password=hashed_password
    )



    db.add(new_user)

    db.commit()



    return {

        "message":
        "Account Created Successfully"
    }





@router.post("/login")

def login(user: UserCreate):

    db: Session = SessionLocal()

    username = user.username.strip()

    password = user.password.strip()



    # LIMIT PASSWORD SIZE

    password = password[:50]



    db_user = db.query(User).filter(
        User.username == username
    ).first()



    if not db_user:

        raise HTTPException(
            status_code=400,
            detail="Invalid username"
        )



    valid = pwd_context.verify(
        password,
        db_user.password
    )



    if not valid:

        raise HTTPException(
            status_code=400,
            detail="Invalid password"
        )



    return {

        "message":
        "Login Successful",

        "username":
        db_user.username
    }