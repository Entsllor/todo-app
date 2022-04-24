from uuid import UUID

from flask import Blueprint
from flask_pydantic import validate

from .. import models
from ..core.database import db
from ..models import AccessToken
from ..schemas.tasks import TaskOut, TaskCreate, TaskUpdate
from ..utils import exceptions
from ..utils.tokens import access_token_required

blueprint = Blueprint("tasks", __name__)


@blueprint.get("/tasks/")
@access_token_required
@validate(response_many=True)
def read_tasks(access_token: AccessToken):
    tasks = models.Task.query.filter_by(user_id=access_token.user_id).all()
    return list(map(TaskOut.from_orm, tasks))


@blueprint.get("/tasks/<string:task_id>")
@access_token_required
@validate()
def read_task(task_id: UUID, access_token: AccessToken):
    task = models.Task.query.get(task_id)
    if task.user_id != access_token.user_id:
        raise exceptions.Forbidden
    return TaskOut.from_orm(task)


@blueprint.post("/tasks/")
@access_token_required
@validate(on_success_status=201)
def create_task(body: TaskCreate, access_token: AccessToken):
    db_task = models.Task(**body.dict(), user_id=access_token.user_id)
    db.session.add(db_task)
    db.session.commit()
    db.session.refresh(db_task)
    return TaskOut.from_orm(db_task)


@blueprint.put("/tasks/<string:task_id>")
@blueprint.patch("/tasks/<string:task_id>")
@access_token_required
@validate(on_success_status=200)
def update_task(body: TaskUpdate, task_id: UUID, access_token: AccessToken):
    # update only if task exists and belongs to current_user
    db.session.query(models.Task). \
        filter_by(id=task_id, user_id=access_token.user_id). \
        update(body.dict(exclude_unset=True))
    db.session.flush()
    task = db.session.query(models.Task).filter_by(id=task_id).first()
    if not task:
        raise exceptions.InstanceNotFound
    if task.user_id != access_token.user_id:
        raise exceptions.Forbidden
    db.session.commit()
    return TaskOut.from_orm(task)
