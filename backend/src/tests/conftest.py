import os

from src.utils.url_utils import get_urls

os.environ["FLASK_ENV"] = "testing"  # noqa

import pytest
from sqlalchemy.orm import Session

from src import crud
from src.app import create_app
from src.core.database import db as _db
from src.core.settings import get_settings
from src.schemas.tokens import AuthTokensOut

DEFAULT_USER_PASSWORD = "default_password"
DEFAULT_USER_LOGIN = "DEFAULT_USERNAME"
USER_CREATE_DATA = {
    'login': DEFAULT_USER_LOGIN,
    'password': DEFAULT_USER_PASSWORD
}

test_app = create_app(get_settings('testing'))
urls = get_urls(test_app)


@pytest.fixture(scope='session')
def app():
    """Session-wide test `Flask` application."""
    app = test_app

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield app
    ctx.pop()


@pytest.fixture(scope='session')
def db(app):
    """Session-wide test database."""
    _db.app = app
    _db.create_all()

    yield _db
    _db.drop_all()


@pytest.fixture(autouse=True)
def session(db) -> Session:
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = {'bind': connection, 'binds': {}}
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session
    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture
def client(app, db):
    return app.test_client(use_cookies=True)


@pytest.fixture
def default_user(session):
    user = crud.Users.create(login=USER_CREATE_DATA['login'], password=USER_CREATE_DATA['password'])
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def second_user(session):
    second_user = crud.Users.create(login="SECOND_LOGIN", password="SECOND_PASSWORD")
    session.commit()
    session.refresh(second_user)
    return second_user


@pytest.fixture
def access_token(default_user):
    return crud.AccessTokens.create(user_id=default_user.id)


@pytest.fixture
def auth_header(access_token) -> dict[str, str]:
    """return authorization header for default user"""
    return {"Authorization": f"Bearer {access_token.body}"}


@pytest.fixture
def token_pair(default_user, access_token) -> AuthTokensOut:
    refresh_token = crud.RefreshTokens.create(user_id=default_user.id)
    return AuthTokensOut(
        expires_in=access_token.expire_at,
        access_token=access_token.body,
        refresh_token=refresh_token.body
    )
