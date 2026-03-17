import os
import secrets
from passlib.context import CryptContext # pyright: ignore[reportMissingModuleSource]
from jose import jwt, JWTError # pyright: ignore[reportMissingModuleSource]
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Header # pyright: ignore[reportMissingImports]
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # pyright: ignore[reportMissingImports]
from app.database import get_db
from app import models
from sqlalchemy.orm import Session # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]

load_dotenv()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not set")

def _normalize_password(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        return password[:60]
    return password

def hash_password(password: str) -> str:
    password = _normalize_password(password)
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password = _normalize_password(plain_password)
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        token = credentials.credentials 
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

        return int(user_id)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

def generate_api_key() -> str:
    return secrets.token_hex(32)

def get_current_project(
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(
        models.Project.api_key == x_api_key
    ).first()

    if not project:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    return project