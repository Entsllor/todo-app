from .. import models
from ..core.database import db
from ..utils import exceptions
from ..utils.passwords import get_password_hash


class UsersCRUD:
    model = models.User

    def get_one(self, **filters) -> models.User:
        return self.model.query.filter_by(**filters)

    def create(self, login: str, password: str) -> models.User:
        hashed_password = get_password_hash(password)
        user_with_same_login = self.model.query.filter_by(login=login).first()
        if user_with_same_login:
            raise exceptions.ExpectedUniqueLogin
        else:
            user = models.User(login=login, hashed_password=hashed_password)
            db.session.add(user)
            return user


Users = UsersCRUD()
