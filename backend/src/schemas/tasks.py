from datetime import datetime
from typing import Optional

from pydantic import BaseModel


def get_optional_schema(base_model_class):
    base_classes = [c for c in base_model_class.__mro__ if (issubclass(c, BaseModel) and c != BaseModel)]
    annotations = {}
    for base_class in base_classes:
        annotations |= base_class.__annotations__
    return {field_name: Optional[annotation] for field_name, annotation in annotations.items()}


class TaskBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class TaskCreate(TaskBase):
    deadline: datetime


class TaskUpdate(TaskCreate):
    __annotations__ = get_optional_schema(TaskCreate)


class TaskOut(TaskCreate):
    created_at: datetime
    id: int
