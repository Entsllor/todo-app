from flask import Flask
from flask_cors import CORS

from src.utils import exceptions
from src.utils.filling_db import fill_db, clear_db
from .core.database import db, migrate
from .core.settings import get_settings
from .routers import tasks, users


def create_app(settings):
    new_app = Flask(__name__)
    new_app.register_blueprint(tasks.blueprint, url_prefix='/api')
    new_app.register_blueprint(users.blueprint, url_prefix='/api/auth/')
    new_app.config["SECRET_KEY"] = settings.SECRET_KEY
    new_app.config["SQLALCHEMY_DATABASE_URI"] = settings.DB_URI
    new_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    new_app.config["TESTING"] = settings.TESTING
    new_app.config["DEBUG"] = settings.TESTING
    new_app.register_error_handler(exceptions.BaseAppException, exceptions.handle_app_exception)
    db.init_app(new_app)
    migrate.init_app(new_app, db, directory=settings.ALEMBIC_PATH)
    CORS(new_app, supports_credentials=True, origins=settings.ALLOWED_ORIGINS)
    return new_app


app = create_app(get_settings())
app.cli.command('fill_db')(fill_db)
app.cli.command('clear_db')(clear_db)

if __name__ == '__main__':
    app.run()
