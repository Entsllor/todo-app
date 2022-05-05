from .base import BaseCrud
from .. import models
from ..core.database import db
from ..utils import exceptions
from ..utils.passwords import get_password_hash


class UsersCRUD(BaseCrud):
    model = models.User

    def create(self, login: str, password: str) -> models.User:
        hashed_password = get_password_hash(password)
        user_with_same_login = self.get_one({"login": login})
        if user_with_same_login:
            raise exceptions.ExpectedUniqueLogin(f"Login '{login}' is already token.")
        else:
            user = models.User(login=login, hashed_password=hashed_password)
            db.session.add(user)
            return user


Users = UsersCRUD()
