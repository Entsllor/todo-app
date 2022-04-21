from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .core.settings import settings


def create_app():
    new_app = Flask(__name__)
    new_app.config["SECRET_KEY"] = settings.SECRET_KEY
    new_app.config["SQLALCHEMY_DATABASE_URI"] = settings.DB_URI
    new_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    return new_app


app = create_app()
db = SQLAlchemy(app=app)


if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
