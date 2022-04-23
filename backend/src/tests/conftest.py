import os
import pytest
from sqlalchemy.orm import Session

from src.app import create_app
from src.core.database import db as _db
from src.core.settings import get_settings

TESTDB = 'test_project.db'
TESTDB_PATH = "/opt/project/data/{}".format(TESTDB)
TEST_DATABASE_URI = 'sqlite:///' + TESTDB_PATH


@pytest.fixture(scope='session')
def app():
    """Session-wide test `Flask` application."""
    os.environ["FLASK_ENV"] = "testing"
    app = create_app(get_settings())

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


@pytest.fixture(scope="session")
def client(app, db):
    return app.test_client(use_cookies=False)
