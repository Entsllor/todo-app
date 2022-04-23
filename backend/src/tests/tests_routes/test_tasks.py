from datetime import datetime, timedelta

import pytest

from src import models

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
NEW_TASK_DATA = {
    'title': "NEW_TASK",
    'description': "DESCRIPTION",
    'deadline': (datetime.now() + timedelta(1)).strftime(DATETIME_FORMAT)
}


def test_create_task(client):
    response = client.post("/tasks/", json=NEW_TASK_DATA)
    new_task = response.json
    assert response.status_code == 201, response.text
    assert new_task['title'] == NEW_TASK_DATA['title']
    assert new_task['description'] == NEW_TASK_DATA['description']
    assert new_task['deadline'] == NEW_TASK_DATA['deadline']


@pytest.fixture(scope="function")
def tasks(db, session):
    new_tasks = [
        models.Task(
            title=f"task_{i}",
            description=f"description_{i}",
            deadline=(datetime.now() + timedelta(i)).strftime(DATETIME_FORMAT)
        )
        for i in range(10)
    ]
    session.add_all(new_tasks)
    session.commit()
    return new_tasks


def test_read_tasks(client, tasks):
    response = client.get("/tasks/")
    assert response.status_code == 200
    tasks_from_response = response.json
    assert len(tasks_from_response) == len(tasks)
    assert tasks_from_response[-1]['title'] == tasks[-1].title


def test_read_task(client, tasks):
    task = tasks[-1]
    response = client.get(f"/tasks/{task.id}")
    assert response.status_code == 200
    task_from_response = response.json
    assert task_from_response['title'] == task.title
    assert task_from_response['deadline'] == task.deadline.strftime(DATETIME_FORMAT)
    assert task_from_response['description'] == task.description


def test_update_task(client, tasks):
    db_task = tasks[-1]
    new_data = {
        "title": db_task.title + "__updated",
        "description": db_task.description + "__updated",
        "deadline": (db_task.deadline + timedelta(1)).strftime(DATETIME_FORMAT)
    }
    response = client.put(f"/tasks/{db_task.id}", json=new_data)
    assert response.status_code == 200
    assert db_task.title == new_data['title']
    assert db_task.description == new_data['description']
    assert db_task.deadline.strftime(DATETIME_FORMAT) == new_data['deadline']


def test_failed_update_task(client, tasks):
    db_task = tasks[-1]
    new_data = {
        "title": db_task.title + "__updated",
        "description": db_task.description + "__updated",
        "deadline": (db_task.deadline + timedelta(1)).strftime(DATETIME_FORMAT)
    }
    response = client.put(f"/tasks/{db_task.id + 10000}", json=new_data)
    assert response.status_code == 404
    assert db_task.title != new_data['title']
    assert db_task.description != new_data['description']
    assert db_task.deadline.strftime(DATETIME_FORMAT) != new_data['deadline']


def test_patch_task(client, tasks):
    db_task = tasks[-1]
    new_data = {
        "title": db_task.title + "__updated",
    }
    response = client.patch(f"/tasks/{db_task.id}", json=new_data)
    assert response.status_code == 200
    assert db_task.title == new_data['title']


def test_failed_patch_task_not_found(client, tasks):
    db_task = tasks[-1]
    new_data = {"title": db_task.title + "__updated", }
    response = client.patch(f"/tasks/{db_task.id + 10000}", json=new_data)
    assert response.status_code == 404
    assert db_task.title != new_data['title']
