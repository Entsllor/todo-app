from src import models
from src.crud.base import BaseCrud


class TaskCrud(BaseCrud):
    model = models.Task


Tasks = TaskCrud()
