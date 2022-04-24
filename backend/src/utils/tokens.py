from functools import wraps

from flask import request

from src import models
from src.utils import exceptions


def access_token_required(_view=None, *, pass_token_to_args=True):
    def wrapper(view):
        @wraps(view)
        def decorated_view(*args, **kwargs):
            authorization_header = request.headers.get("Authorization", "")
            match authorization_header.split(" "):
                case _, token:
                    access_token = models.AccessToken(token)
                case _:
                    raise exceptions.AccessTokenRequiredError
            access_token.validate()
            if pass_token_to_args:
                return view(*args, access_token=access_token, **kwargs)
            return view(*args, **kwargs)

        return decorated_view

    if _view:
        return wrapper(_view)
    return wrapper
