import os
from datetime import datetime, timedelta
from uuid import UUID # Added UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import bcrypt
from jose import jwt


SECRET_KEY = os.environ.get("JWT_SECRET", "dev-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


class Giga:
    """Small replacement for the original Giga helper used for password hashing."""

    @staticmethod
    def get_password_hash(password: str) -> str:
        # Use the native bcrypt library directly to avoid passlib backend detection issues.
        pw_bytes = password.encode("utf-8")[:72]
        hashed = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        pw_bytes = plain_password.encode("utf-8")[:72]
        try:
            return bcrypt.checkpw(pw_bytes, hashed_password.encode("utf-8"))
        except Exception:
            # Fallback to passlib verify if needed
            try:
                return pwd_context.verify(plain_password, hashed_password)
            except Exception:
                return False


def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode = data.copy()
    # Convert user_id to str for JWT encoding
    if "user_id" in to_encode and isinstance(to_encode["user_id"], UUID):
        to_encode["user_id"] = str(to_encode["user_id"])
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithms=[ALGORITHM])


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id_str: str = payload.get("user_id") # Get as string
        if username is None or user_id_str is None:
            raise credentials_exception
        user_id: UUID = UUID(user_id_str) # Convert to UUID
        return {"username": username, "user_id": user_id}
    except jwt.PyJWTError:
        raise credentials_exception