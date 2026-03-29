import jwt
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from pwdlib import PasswordHash
from Models.models import User, UserCreate, UserPublic, UserRole, Role

from Services.log_service import log_new_user

load_dotenv()
with open('private_key.pem', 'r') as f:
    PRIVATE_KEY = f.read()
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")

from datetime import datetime, timedelta, timezone

def fake_hash_password(password: str):
    return "fakehashed" + password


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expires_delta = timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        PRIVATE_KEY,
        algorithm=ALGORITHM)
    return encoded_jwt


def get_user(user_id: str, session):
    user = session.query(User).filter(User.user_id == user_id).first()
    if user:
        return UserPublic(id=user.user_id, email=user.email)
    return None


def authenticate_user(email: str, password: str, session):
    user = session.query(User).filter(User.email == email).first()
    if not user or not user.is_active:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_user(user, session):
    user_create = UserCreate.model_validate(user)

    hashed_password = get_password_hash(user_create.password)

    user_db = User(email=user_create.email, hashed_password=hashed_password)
    user_db.roles.append(UserRole(role=Role.USER))
    session.add(user_db)

    try:
        session.commit()
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )

    session.refresh(user_db)
    log_new_user(user_db)
    return UserPublic(email=user_db.email, user_id=user_db.user_id)
