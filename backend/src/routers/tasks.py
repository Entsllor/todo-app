from uuid import UUID

from flask_pydantic import validate
from flask import Blueprint, abort
from .. import models
from ..schemas.tasks import TaskOut, TaskCreate, TaskUpdate
from ..core.database import db

blueprint = Blueprint("tasks", __name__)


@blueprint.get("/tasks/")
@validate(response_many=True)
def read_tasks():
    tasks = models.Task.query.all()
    return list(map(TaskOut.from_orm, tasks))


@blueprint.get("/tasks/<string:task_id>")
@validate()
def read_task(task_id: UUID):
    task = models.Task.query.get(task_id)
    return TaskOut.from_orm(task)


@blueprint.post("/tasks/")
@validate(on_success_status=201)
def create_task(body: TaskCreate):
    db_task = models.Task(**body.dict())
    db.session.add(db_task)
    db.session.commit()
    db.session.refresh(db_task)
    return TaskOut.from_orm(db_task)


@blueprint.put("/tasks/<string:task_id>")
@blueprint.patch("/tasks/<string:task_id>")
@validate(on_success_status=200)
def update_task(body: TaskUpdate, task_id: UUID):
    updated = db.session.query(models.Task).filter_by(id=task_id).update(body.dict())
    db.session.commit()
    if not updated:
        abort(404)
    return '', 200
