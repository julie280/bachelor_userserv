import os
from dotenv import load_dotenv

from sqlalchemy import Engine
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
    engine_azure = create_engine(f"odbcapi+mssql://{user}:{password}@{server}/{database}" )
    return engine_azure

#load_dotenv()
#DATABASE_URL = "postgresql://postgres:uUP;(m_hCb>&mA4(q/BR@localhost/julie_ba"
#engine = create_engine(DATABASE_URL, echo=True)
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