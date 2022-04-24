from uuid import UUID

from .. import models, crud
from ..utils import exceptions


def authorize_by_login_and_password(login: str, password: str) -> models.User:
    user = crud.Users.get_one(login=login).first()
    if not user or not user.password_match(plain_password=password):
        raise exceptions.IncorrectLoginOrPassword
    return user


def create_auth_token_pair(user_id: UUID | str) -> tuple[models.AccessToken, models.RefreshToken]:
    access_token = crud.AccessTokens.create(user_id)
    refresh_token = crud.RefreshTokens.create(user_id)
    return access_token, refresh_token


def revoke_tokens(user_id: UUID | str, refresh_token_body: str) -> tuple[models.AccessToken, models.RefreshToken]:
    valid_token = crud.RefreshTokens.get_valid_token(user_id=user_id, body=refresh_token_body)
    if valid_token:
        return create_auth_token_pair(user_id)
    else:
        raise exceptions.CredentialsException
