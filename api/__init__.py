from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from Auth.auth import authenticate_user, create_access_token, create_user
from Models.models import Token, UserCreate, UserPublic, UserBase
from Services.db_service import create_db_and_tables, SessionDep, delete_user, read_user_data

app = FastAPI(
    title="API-User-service",
    description="This is Pilot setup",
    version="1.0.1",
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/user/hello/{user_id}")
def hello(user_id: str):
    return {"message": f"Hello World {user_id}"}


@app.post("/user/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": str(user.user_id), "email": user.email, "roles": [role.role.value for role in user.roles]})
    return Token(access_token=access_token, token_type="bearer")


@app.post("/user/register", response_model=UserPublic)
# Please note: Only for testing. No Validation
def user_register(user: UserCreate, session: SessionDep):
    return create_user(user, session)


@app.get("/user/dataInfo")
def get_user_data_info():
    data_info = {
        "category": "Accountdaten",
        "purpose": "Authentifizierung, Autorisierung",
        "duration_of_storage": "Speicherung erfolgt bis der Account gelöscht wird",
        "destination": ""
    }
    return data_info

@app.get("/user/userData/{user_id}", response_model=UserBase)
def get_user_data(user_id: str, session: SessionDep):
    return read_user_data(user_id, session)

@app.delete("/user/userData/{user_id}")
def delete_user_data(user_id: str, session: SessionDep):
    return delete_user(user_id, session)

