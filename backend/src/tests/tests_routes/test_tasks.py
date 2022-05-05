from datetime import datetime, timedelta

import pytest
from sqlalchemy.orm.exc import ObjectDeletedError

from src import models
from src.schemas.tasks import TaskOut

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
TASKS_URL = 'api/tasks/'
TASK_URL = TASKS_URL + "{}"
NEW_TASK_DATA = {
    'title': "NEW_TASK",
    'description': "DESCRIPTION",
    'deadline': (datetime.now() + timedelta(1)).strftime(DATETIME_FORMAT)
}
WRONG_UUID = "00000000-0000-0000-0000-000000000000"


def test_create_task(client, auth_header):
    response = client.post(f"{TASKS_URL}", json=NEW_TASK_DATA, headers=auth_header)
    new_task = response.json
    assert response.status_code == 201, response.text
    assert new_task['title'] == NEW_TASK_DATA['title']
    assert new_task['description'] == NEW_TASK_DATA['description']
    assert new_task['deadline'] == NEW_TASK_DATA['deadline']
    assert new_task['status'] == 'pending'
    TaskOut(**response.json)  # validate response body


def test_failed_create_task_unauthorized(client):
    response = client.post(f"{TASKS_URL}", json=NEW_TASK_DATA)
    assert response.status_code == 401, response.text


@pytest.fixture(scope="function")
def tasks(session, default_user, second_user):
    new_tasks = [
        models.Task(
            title=f"task_{i}",
            description=f"description_{i}",
            deadline=(datetime.now() + timedelta(i)).strftime(DATETIME_FORMAT),
            user_id=default_user.id if i <= 10 else second_user.id
        )
        for i in range(1, 21)
    ]
    session.add_all(new_tasks)
    session.commit()
    return new_tasks


def test_read_tasks(client, tasks, auth_header, default_user):
    response = client.get(f"{TASKS_URL}", headers=auth_header)
    assert len(tasks) != len(default_user.tasks)
    assert response.status_code == 200, response.text
    tasks_from_response = response.json
    tasks_from_response_ids = {task['id'] for task in tasks_from_response}
    tasks_from_db_ids = {str(task.id) for task in default_user.tasks}
    assert len(tasks_from_response) == len(default_user.tasks)
    assert tasks_from_db_ids == tasks_from_response_ids


def test_read_tasks_unauthorized(client, tasks):
    response = client.get(f"{TASKS_URL}")
    assert response.status_code == 401, response.text


def test_read_task(client, tasks, auth_header, default_user):
    task = default_user.tasks[-1]
    response = client.get(f"{TASKS_URL}{task.id}", headers=auth_header)
    assert response.status_code == 200, response.text
    task_from_response = response.json
    assert task_from_response['title'] == task.title
    assert task_from_response['deadline'] == task.deadline.strftime(DATETIME_FORMAT)
    assert task_from_response['description'] == task.description
    assert task_from_response['status'] == task.status


def test_failed_read_foreign_task(client, tasks, auth_header, second_user):
    task = second_user.tasks[-1]
    response = client.get(f"{TASKS_URL}{task.id}", headers=auth_header)
    assert response.status_code == 403, response.text


def test_read_task_unauthorized(client, tasks):
    response = client.get(f"{TASKS_URL}{tasks[-1].id}")
    assert response.status_code == 401, response.text


def test_update_task(client, tasks, auth_header, default_user):
    db_task = default_user.tasks[-1]
    new_data = {
        "title": db_task.title + "__updated",
        "description": db_task.description + "__updated",
        "deadline": (db_task.deadline + timedelta(1)).strftime(DATETIME_FORMAT)
    }
    response = client.put(f"{TASKS_URL}{db_task.id}", json=new_data, headers=auth_header)
    assert response.status_code == 200, response.text
    assert db_task.title == new_data['title']
    assert db_task.description == new_data['description']
    assert db_task.deadline.strftime(DATETIME_FORMAT) == new_data['deadline']
    assert TaskOut(**response.json)


def test_failed_update_foreign_task(client, tasks, auth_header, second_user):
    db_task = second_user.tasks[-1]
    new_data = {
        "title": db_task.title + "__updated",
        "description": db_task.description + "__updated",
        "deadline": (db_task.deadline + timedelta(1)).strftime(DATETIME_FORMAT)
    }
    response = client.put(f"{TASKS_URL}{db_task.id}", json=new_data, headers=auth_header)
    assert response.status_code == 403, response.text
    assert response.json['error_description'] == "You can update only your own tasks"


def test_failed_update_task_unauthorized(client, tasks, default_user):
    db_task = default_user.tasks[-1]
    new_data = {
        "title": db_task.title + "__updated",
        "description": db_task.description + "__updated",
        "deadline": (db_task.deadline + timedelta(1)).strftime(DATETIME_FORMAT)
    }
    response = client.put(f"{TASKS_URL}{db_task.id}", json=new_data)
    assert response.status_code == 401, response.text


def test_failed_update_task_not_found(client, tasks, auth_header, default_user):
    db_task = default_user.tasks[-1]
    new_data = {
        "title": db_task.title + "__updated",
        "description": db_task.description + "__updated",
        "deadline": (db_task.deadline + timedelta(1)).strftime(DATETIME_FORMAT)
    }
    response = client.put(f"{TASKS_URL}{WRONG_UUID}", json=new_data, headers=auth_header)
    assert response.status_code == 404
    assert db_task.title != new_data['title']
    assert db_task.description != new_data['description']
    assert db_task.deadline.strftime(DATETIME_FORMAT) != new_data['deadline']


def test_patch_task(client, tasks, auth_header, default_user):
    db_task = default_user.tasks[-1]
    new_data = {"title": db_task.title + "__updated"}
    response = client.patch(f"{TASKS_URL}{db_task.id}", json=new_data, headers=auth_header)
    assert response.status_code == 200, response.text
    assert db_task.title == new_data['title']
    assert TaskOut(**response.json)


def test_failed_patch_foreign_task(client, tasks, auth_header, second_user):
    db_task = second_user.tasks[-1]
    new_data = {"title": db_task.title + "__updated"}
    response = client.patch(f"{TASKS_URL}{db_task.id}", json=new_data, headers=auth_header)
    assert response.status_code == 403, response.text
    assert response.json['error_description'] == "You can update only your own tasks"


def test_failed_patch_task_unauthorized(client, tasks, default_user):
    db_task = default_user.tasks[-1]
    new_data = {"title": db_task.title + "__updated"}
    response = client.patch(f"{TASKS_URL}{db_task.id}", json=new_data)
    assert response.status_code == 401, response.text


def test_failed_patch_task_not_found(client, tasks, auth_header, default_user):
    db_task = default_user.tasks[-1]
    new_data = {"title": db_task.title + "__updated"}
    response = client.patch(f"{TASKS_URL}{WRONG_UUID}", json=new_data, headers=auth_header)
    assert response.status_code == 404
    assert db_task.title != new_data['title']


def test_patch_set_task_completed(client, tasks, auth_header, default_user):
    db_task = default_user.tasks[-1]
    assert not db_task.is_completed
    new_data = {"is_completed": True}
    response = client.patch(f"{TASKS_URL}{db_task.id}", json=new_data, headers=auth_header)
    assert response.status_code == 200, response.text
    assert db_task.is_completed
    assert db_task.status == 'completed'


def test_delete_task(client, tasks, auth_header, default_user, session):
    db_task = default_user.tasks[-1]
    response = client.delete(TASK_URL.format(db_task.id), headers=auth_header)
    assert response.status_code == 204
    with pytest.raises(ObjectDeletedError):
        assert db_task.id


def test_failed_delete_task_not_found(client, tasks, auth_header, default_user):
    response = client.delete(TASK_URL.format(WRONG_UUID), headers=auth_header)
    assert response.status_code == 403


def test_failed_delete_foreign_task(client, tasks, auth_header, second_user):
    db_task = second_user.tasks[-1]
    response = client.delete(TASK_URL.format(db_task.id), headers=auth_header)
    assert response.status_code == 403
    assert response.json['error_description'] == "You can delete only your own tasks"


def test_failed_delete_task_unauthorized(client, tasks, default_user):
    db_task = default_user.tasks[-1]
    response = client.delete(TASK_URL.format(db_task.id))
    assert response.status_code == 401
