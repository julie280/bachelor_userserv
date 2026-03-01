from datetime import timedelta
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
import os
from dotenv import load_dotenv

from Auth.auth import get_user, authenticate_user, create_access_token, create_user
from Models.models import TokenData, User, Token, UserCreate, UserPublic
from Services.db_service import  create_db_and_tables, SessionDep

app = FastAPI(
   title="API-Gateway",
    description="This is Pilot setup",
    version="1.0.1",
   )

with open('private_key.pem', 'r') as f:
    PRIVATE_KEY = f.read()

with open('public_key.pem', 'r') as f:
    PUBLIC_KEY = f.read()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

load_dotenv()
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, email=payload.get("email"), roles=payload.get("roles"))
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(user_id=token_data.user_id, session=session)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],session: SessionDep
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "roles": [role.role.value for role in user.roles] }, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/user/me",response_model=UserPublic)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user

@app.post("/user/register", response_model=UserPublic)
#Please note: Only for testing. No Validation
def user_register(user: UserCreate, session: SessionDep):
    return create_user(user,session)
