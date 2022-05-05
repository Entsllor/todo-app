from uuid import UUID

from flask import Blueprint
from flask_pydantic import validate

from .. import models, crud
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
    tasks = crud.Tasks.get_many({'user_id': access_token.user_id})
    return list(map(TaskOut.from_orm, tasks))


@blueprint.get("/tasks/<string:task_id>")
@access_token_required
@validate()
def read_task(task_id: UUID, access_token: AccessToken):
    task = crud.Tasks.get_by_id(task_id)
    if task.user_id != access_token.user_id:
        raise exceptions.Forbidden("You can read only your own tasks")
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


@blueprint.delete("/tasks/<string:task_id>")
@access_token_required
def delete_task(access_token: AccessToken, task_id: UUID):
    deleted = crud.Tasks.delete({'id': task_id, 'user_id': access_token.user_id})
    if not deleted:
        raise exceptions.Forbidden("You can delete only your own tasks")
    db.session.commit()
    return "", 204


@blueprint.put("/tasks/<string:task_id>")
@blueprint.patch("/tasks/<string:task_id>")
@access_token_required
@validate()
def update_task(body: TaskUpdate, task_id: UUID, access_token: AccessToken):
    # update only if task exists and belongs to current_user
    crud.Tasks.update(values=body.dict(exclude_unset=True), filters={'id': task_id, 'user_id': access_token.user_id})
    db.session.flush()
    task = crud.Tasks.get_by_id(task_id)
    if not task:
        raise exceptions.InstanceNotFound(f"Failed to find task with id={UUID}")
    if task.user_id != access_token.user_id:
        raise exceptions.Forbidden("You can update only your own tasks")
    db.session.commit()
    return TaskOut.from_orm(task)
