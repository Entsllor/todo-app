import time

import pytest
from pydantic import ValidationError

from src import models, crud
from src.schemas.tokens import AuthTokensOut
from src.tests.conftest import SIGN_UP_URL, LOGIN_URL, REVOKE_URL, DEFAULT_USER_PASSWORD, USER_CREATE_DATA, LOGOUT_URL


def test_create_user(client, session):
    response = client.post(SIGN_UP_URL, json=USER_CREATE_DATA)
    assert response.status_code == 201, response.text
    created_user = response.json
    assert created_user['login'] == USER_CREATE_DATA['login']
    # check password is hashed
    db_user = models.User.query.get(created_user['id'])
    assert db_user.hashed_password != USER_CREATE_DATA['password']
    # check api does not return password
    assert not (created_user.get('password') or created_user.get('hashed_password'))
    assert created_user['id']
    assert created_user['created_at']


def test_failed_create_user_not_unique_login(client, default_user):
    response = client.post(SIGN_UP_URL, json=USER_CREATE_DATA)
    assert response.status_code == 400, response.text
    assert f"Login '{default_user.login}' is already token." in response.json['error_description']


def test_login(default_user, client):
    response = client.post(
        LOGIN_URL,
        json={'login': default_user.login, 'password': DEFAULT_USER_PASSWORD},
    )
    assert response.status_code == 200, response.text
    assert AuthTokensOut(**response.json)  # validate response content


def test_failed_login_wrong_password(default_user, client):
    response = client.post(LOGIN_URL, json={'login': default_user.login, 'password': "__WRONG_PASSWORD"})
    assert response.status_code == 401, response.text
    with pytest.raises(ValidationError):
        assert AuthTokensOut(**response.json)  # validate response content


def test_failed_login_user_does_not_exist(default_user, client):
    response = client.post(LOGIN_URL, json={'login': "__WRONG_USERNAME", 'password': DEFAULT_USER_PASSWORD})
    assert response.status_code == 401, response.text
    with pytest.raises(ValidationError):
        assert AuthTokensOut(**response.json)  # validate response content


def test_revoke_tokens(client, token_pair, default_user):
    client.set_cookie('test', "refresh_token", token_pair.refresh_token)
    client.set_cookie('test', "client_id", str(default_user.id))
    response = client.post(REVOKE_URL)
    assert response.status_code == 200, response.text
    assert AuthTokensOut(**response.json)


def test_failed_revoke_tokens_if_refresh_token_expired(client, token_pair, default_user):
    client.set_cookie('test', "refresh_token", token_pair.refresh_token)
    client.set_cookie('test', "client_id", str(default_user.id))
    crud.RefreshTokens.change_expire_term(default_user.id, token_pair.refresh_token, time.time() - 100)
    response = client.post(REVOKE_URL)
    assert response.status_code == 401, response.text


def test_failed_revoke_tokens_if_refresh_token_invalid(client, token_pair, default_user):
    client.set_cookie('test', "refresh_token", token_pair.refresh_token + "_invalid")
    client.set_cookie('test', "client_id", str(default_user.id))
    crud.RefreshTokens.change_expire_term(default_user.id, token_pair.refresh_token, time.time() - 100)
    response = client.post(REVOKE_URL)
    assert response.status_code == 401, response.text


def test_failed_revoke_tokens_if_refresh_token_belongs_to_another_user(client, token_pair):
    another_user = crud.Users.create(login="ANOTHER_USER", password="Another_Password")
    client.set_cookie('test', "refresh_token", token_pair.refresh_token + "_invalid")
    client.set_cookie('test', "client_id", str(another_user.id))
    response = client.post(REVOKE_URL)
    assert response.status_code == 401, response.text


def test_failed_revoke_client_id_required(client, token_pair, default_user):
    client.set_cookie('test', "client_id", str(default_user.id))
    response = client.post(REVOKE_URL)
    assert response.status_code == 401, response.text


def test_failed_revoke_client_refresh_token_required(client, token_pair):
    client.set_cookie('test', "refresh_token", token_pair.refresh_token)
    response = client.post(REVOKE_URL)
    assert response.status_code == 401, response.text


def test_logout(client, token_pair, default_user):
    client.set_cookie('test', "refresh_token", token_pair.refresh_token)
    client.set_cookie('test', "client_id", str(default_user.id))
    response = client.post(LOGOUT_URL)
    assert response.status_code == 204, response.text


def test_failed_logout_client_id_required(client, token_pair, default_user):
    client.set_cookie('test', "client_id", str(default_user.id))
    response = client.post(LOGOUT_URL)
    assert response.status_code == 401, response.text


def test_failed_logout_client_refresh_token_required(client, token_pair):
    client.set_cookie('test', "refresh_token", token_pair.refresh_token)
    response = client.post(LOGOUT_URL)
    assert response.status_code == 401, response.text
