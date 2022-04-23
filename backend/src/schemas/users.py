from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserLogin(BaseModel):
    login: str
    password: str

    class Config:
        orm_mode = True


class UserCreate(UserLogin):
    pass


class UserOut(BaseModel):
    login: str
    created_at: datetime
    id: str | UUID

    class Config:
        orm_mode = True
