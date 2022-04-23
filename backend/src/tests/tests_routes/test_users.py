import pytest

from src import models
from src.utils.passwords import get_password_hash

USER_CREATE_DATA = {
    'login': 'DEFAULT_USERNAME',
    'password': "default_password"
}


def test_create_user(client, session):
    response = client.post('/sign-up', json=USER_CREATE_DATA)
    assert response.status_code == 201, response.text
    created_user = response.json
    assert created_user['login'] == USER_CREATE_DATA['login']
    # check password is hashed
    db_user = models.User.query.get(created_user['id'])
    assert db_user.hashed_password != USER_CREATE_DATA['password']
    # check api does not return password
    assert not (created_user.get('password') or created_user.get('hashed_password'))
    assert created_user['id']
    assert created_user['created_at']


@pytest.fixture
def default_user(session):
    hashed_password = get_password_hash(USER_CREATE_DATA['password'])
    user = models.User(login=USER_CREATE_DATA['login'], hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def test_failed_create_user_not_unique_username(client, default_user):
    response = client.post('/sign-up', json=USER_CREATE_DATA)
    assert response.status_code == 400, response.text
