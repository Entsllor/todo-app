import time
from uuid import UUID

from jose import jwt

from .base import BaseCrud
from .. import models
from ..core.database import db
from ..core.settings import get_settings


class RefreshTokenCRUD(BaseCrud):
    model = models.RefreshToken

    def create(self, user_id, expire_delta: int = None) -> models.RefreshToken:
        self.delete({"user_id": user_id})
        if expire_delta is None:
            expire_delta = get_settings().REFRESH_TOKEN_EXPIRE_SECONDS
        expire_at = time.time() + expire_delta
        refresh_token = self.model(user_id=user_id, expire_at=expire_at)
        db.session.add(refresh_token)
        db.session.flush([refresh_token])
        return refresh_token

    def get_by_body_and_user_id(self, user_id: UUID, body: str) -> models.RefreshToken | None:
        return self.model.query.where(self.model.user_id == user_id, self.model.body == body)

    def get_valid_token(self, user_id: UUID, body: str) -> models.RefreshToken | None:
        return self.model.query.where(
            self.model.user_id == user_id,
            self.model.body == body,
            self.model.expire_at >= time.time()
        ).first()

    def change_expire_term(self, user_id: UUID, token_body: str, expire_at: int):
        return self.model.query. \
            where(self.model.user_id == user_id, self.model.body == token_body). \
            update({'expire_at': expire_at})


class AccessTokenCRUD:
    @staticmethod
    def create_with_custom_data(data: dict = None, expire_delta: int = None) -> models.AccessToken:
        if data is None:
            data = dict()
        if expire_delta is None:
            expire_delta = get_settings().REFRESH_TOKEN_EXPIRE_SECONDS
        expire_at = time.time() + expire_delta
        data["exp"] = expire_at
        body = jwt.encode(data, get_settings().SECRET_KEY, algorithm=get_settings().JWT_ALGORITHM)
        return models.AccessToken(body=body)

    def create(self, user_id: int, expire_delta: int = None) -> models.AccessToken:
        return self.create_with_custom_data(data={'sub': str(user_id)}, expire_delta=expire_delta)


AccessTokens = AccessTokenCRUD()
RefreshTokens = RefreshTokenCRUD()
