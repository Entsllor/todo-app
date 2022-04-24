from flask import Flask

from src.utils import exceptions
from .core.database import db, migrate
from .core.settings import get_settings
from .routers import tasks, users


def create_app(settings):
    new_app = Flask(__name__)
    new_app.register_blueprint(tasks.blueprint)
    new_app.register_blueprint(users.blueprint)
    new_app.config["SECRET_KEY"] = settings.SECRET_KEY
    new_app.config["SQLALCHEMY_DATABASE_URI"] = settings.DB_URI
    new_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    new_app.config["TESTING"] = settings.TESTING
    new_app.config["DEBUG"] = settings.TESTING
    new_app.register_error_handler(exceptions.BaseAppException, exceptions.handle_app_exception)
    db.init_app(new_app)
    migrate.init_app(new_app, db, directory=settings.ALEMBIC_PATH)
    return new_app


app = create_app(get_settings())

if __name__ == '__main__':
    app.run()
