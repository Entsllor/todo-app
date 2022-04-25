from datetime import datetime
from uuid import UUID

from flask import Blueprint, request, make_response
from flask_pydantic import validate
from flask_pydantic.core import make_json_response

from .. import crud
from ..core.database import db
from ..schemas.tokens import AuthTokensOut
from ..schemas.users import UserCreate, UserOut, UserLogin
from ..services import auth
from ..utils import exceptions

blueprint = Blueprint('users', __name__)
REVOKE_URL = "/revoke"


@blueprint.post("/sign-up")
@validate(on_success_status=201)
def create_user(body: UserCreate):
    db_user = crud.Users.create(login=body.login, password=body.password)
    db.session.commit()
    db.session.refresh(db_user)
    return UserOut.from_orm(db_user)


@blueprint.post("/logout")
def logout():
    refresh_token = request.cookies.get("refresh_token")
    try:
        user_id = UUID(request.cookies.get("client_id"))
        if not refresh_token:
            raise ValueError
    except (ValueError, TypeError):
        raise exceptions.CredentialsException
    crud.RefreshTokens.delete({'body': refresh_token, 'user_id': user_id})
    response = make_response("", 204)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=0,
        httponly=True
    )
    response.set_cookie(
        key="client_id",
        value=str(user_id),
        expires=0,
        httponly=True
    )
    db.session.commit()
    return response


@blueprint.post("/login")
@validate()
def login(body: UserLogin):
    user = auth.authorize_by_login_and_password(login=body.login, password=body.password)
    access_token, refresh_token, = auth.create_auth_token_pair(user_id=user.id)
    content = AuthTokensOut(
        access_token=access_token.body,
        refresh_token=refresh_token.body,
        expires_in=datetime.fromtimestamp(access_token.expire_at)
    )
    response = make_json_response(content, 200, by_alias=False)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token.body,
        expires=refresh_token.expire_at,
        path='api/auth/',
        httponly=True
    )
    response.set_cookie(
        key="client_id",
        value=str(user.id),
        expires=refresh_token.expire_at,
        path='api/auth/',
        httponly=True
    )
    return response


@blueprint.post(REVOKE_URL)
@validate()
def revoke():
    refresh_token = request.cookies.get("refresh_token")
    try:
        user_id = UUID(request.cookies.get("client_id"))
        if not refresh_token:
            raise ValueError
    except (ValueError, TypeError):
        raise exceptions.CredentialsException
    access_token, refresh_token = auth.revoke_tokens(user_id=user_id, refresh_token_body=refresh_token)
    db.session.commit()
    content = AuthTokensOut(
        access_token=access_token.body,
        refresh_token=refresh_token.body,
        expires_in=datetime.fromtimestamp(access_token.expire_at)
    )
    response = make_json_response(content, 200, by_alias=False)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token.body,
        expires=refresh_token.expire_at,
        path='api/auth/',
        httponly=True
    )
    response.set_cookie(
        key="client_id",
        value=str(access_token.user_id),
        expires=refresh_token.expire_at,
        path='api/auth/',
        httponly=True
    )
    return response
