import os
from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel
from sqlalchemy.orm import Session

import app.models
from app.database import SessionLocal

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not set in .env")

ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

auth = APIRouter(tags=["Authentication"])
password_hasher = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class Registration(BaseModel):
    name: str
    email: str
    password: str


@auth.post("/register", status_code=status.HTTP_201_CREATED)
def registration(new_user: Registration, db: db_dependency):
    email = new_user.email.strip().lower()

    existing = db.query(app.models.User).filter(
        app.models.User.email == email
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="User already exists")

    user_record = app.models.User(
        name=new_user.name.strip(),
        email=email,
        role="customer",
        password=password_hasher.hash(new_user.password),
    )
    db.add(user_record)
    db.commit()

    return {"message": "User registered successfully"}


@auth.post("/login")
def login_credentials(
    db: db_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    email = form_data.username.strip().lower()

    user = db.query(app.models.User).filter(
        app.models.User.email == email
    ).first()

    invalid = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if user is None:
        raise invalid

    try:
        valid = password_hasher.verify(form_data.password, user.password)
    except Exception:
        # stored value is not a valid hash (old/plain-text/truncated)
        raise invalid

    if not valid:
        raise invalid

    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "role": str(user.role),
        "iat": now,
        "exp": now + timedelta(minutes=TOKEN_EXPIRE_MINUTES),
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}


def verify_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )