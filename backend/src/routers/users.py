from datetime import datetime
from uuid import UUID

from flask import Blueprint, request
from flask_pydantic import validate

from src import crud
from src.core.database import db
from src.schemas.tokens import AuthTokensOut
from src.schemas.users import UserCreate, UserOut, UserLogin
from src.services import auth
from src.utils import exceptions

blueprint = Blueprint('users', __name__)


@blueprint.post("/sign-up")
@validate(on_success_status=201)
def create_user(body: UserCreate):
    db_user = crud.Users.create(login=body.login, password=body.password)
    db.session.commit()
    db.session.refresh(db_user)
    return UserOut.from_orm(db_user)


@blueprint.post("/login")
@validate(on_success_status=200)
def login(body: UserLogin):
    user = auth.authorize_by_login_and_password(login=body.login, password=body.password)
    access_token, refresh_token = auth.create_auth_token_pair(user_id=user.id)
    return AuthTokensOut(
        access_token=access_token.body,
        refresh_token=refresh_token.body,
        expires_in=datetime.fromtimestamp(access_token.expire_at)
    )


@blueprint.post("/revoke")
@validate()
def revoke():
    refresh_token = request.cookies.get("refresh_token")
    try:
        user_id = UUID(request.cookies.get("client_id"))
        if not refresh_token:
            raise ValueError
    except ValueError:
        raise exceptions.CredentialsException
    access_token, refresh_token = auth.revoke_tokens(user_id=user_id, refresh_token_body=refresh_token)
    db.session.commit()
    return AuthTokensOut(
        access_token=access_token.body,
        refresh_token=refresh_token.body,
        expires_in=datetime.fromtimestamp(access_token.expire_at)
    )
