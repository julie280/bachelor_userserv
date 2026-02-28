from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class UserBase(SQLModel):
    email: EmailStr = Field(index=True)

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(...)
    hashed_password: str = Field(...)

class UserPublic(UserBase):
    id:int
    email: EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
