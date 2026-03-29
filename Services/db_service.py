import os
from dotenv import load_dotenv

from sqlalchemy import Engine, URL
from typing import Annotated
from fastapi import Depends, HTTPException
from sqlmodel import Session, SQLModel, create_engine

from Models.models import User, UserBase


def get_engine_azure() -> Engine:
    load_dotenv()
    server = os.getenv('SERVER_NAME')
    database = os.getenv('DATABASE')
    user = os.getenv('UID')
    password = os.getenv('PASSWORD')
    driver = "{ODBC Driver 18 for SQL Server}"

    connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password}"
    connection_url = URL.create(
        "mssql+pyodbc", query={"odbc_connect": connection_string}
    )
    return create_engine(connection_url)


engine = get_engine_azure()


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


SessionDep = Annotated[Session, Depends(get_session)]


def delete_user(user_id: str, session: Session):
    user_data = session.get(User, user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user_data)
    session.commit()
    return {"ok": True}


def read_user_data(user_id: str, session: Session):
    user_data = session.get(User, user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return UserBase.model_validate(user_data)


def deactivate_user(user_id: str, session: Session):
    user_data = session.get(User, user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    user_data.is_active = False
    session.add(user_data)
    session.commit()
    return {"ok": True}
