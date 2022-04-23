from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


def get_optional_schema(base_model_class):
    """Makes all fields optional.
    class UserUpdate(UserCreate):
        __annotations__ = get_optional_schema(UserCreate)
        new_field: ...  # describe other fields only after __annotations__ setting.
    """
    base_classes = [c for c in base_model_class.__mro__ if (issubclass(c, BaseModel) and c != BaseModel)]
    annotations = {}
    for base_class in base_classes:
        annotations |= base_class.__annotations__
    return {field_name: Optional[annotation] for field_name, annotation in annotations.items()}


class TaskBase(BaseModel):
    title: str
    description: str | None

    class Config:
        orm_mode = True


class TaskCreate(TaskBase):
    deadline: datetime


class TaskUpdate(TaskCreate):
    __annotations__ = get_optional_schema(TaskCreate)
    is_completed: bool | None


class TaskOut(TaskCreate):
    status: str
    is_completed: bool
    created_at: datetime
    id: UUID
