import uuid
from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel, Relationship
from enum import StrEnum


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: uuid.UUID | None = None
    email: str | None = None
    roles: list["UserRole"] | None = None


class UserBase(SQLModel):
    email: EmailStr = Field(index=True)


class User(UserBase, table=True):
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, max_length=5)
    email: EmailStr = Field(...)
    hashed_password: str = Field(...)

    roles: list["UserRole"] = Relationship(back_populates="user", cascade_delete=True)


class UserPublic(UserBase):
    user_id: uuid.UUID
    email: EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Role(StrEnum):
    ADMIN = 'admin'
    USER = 'user'


class UserRole(SQLModel, table=True):
    user_id: uuid.UUID = Field(foreign_key="user.id", primary_key=True, ondelete="CASCADE")
    role: Role = Field(primary_key=True)
    user: User = Relationship(back_populates="roles")
