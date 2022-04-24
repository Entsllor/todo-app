import http

STATUS_DESCRIPTIONS = {i_status.value: i_status.description for i_status in list(http.HTTPStatus)}


class HTTPException(Exception):
    def __init__(self, message: str = "", status_code: int = 400):
        if not message:
            message = STATUS_DESCRIPTIONS.get(status_code, "")
        self.status_code = status_code
        self.message = message


class BaseAppException(Exception):
    as_http: HTTPException


def handle_app_exception(exception: BaseAppException):
    status_code = 500
    message = "Internal Server Error. Please report this error admin@example.com"
    if hasattr(exception, "as_http"):
        status_code = exception.as_http.status_code
        message = exception.as_http.message
    return {"error_code": status_code, "error_description": message}, status_code


class IncorrectLoginOrPassword(BaseAppException):
    as_http = HTTPException(
        status_code=401,
        message="Incorrect username or password",
    )


class CredentialsException(BaseAppException):
    as_http = HTTPException(
        status_code=401,
        message="Could not validate credentials"
    )


class InactiveUser(BaseAppException):
    as_http = HTTPException(
        status_code=401,
        message="Current user is inactive"
    )


class UserNotFoundError(BaseAppException):
    as_http = HTTPException(
        status_code=401,
        message="Failed to find this User"
    )


class Forbidden(BaseAppException):
    as_http = HTTPException(
        status_code=403,
        message="Sorry, but you do not have enough rights"
    )


class ExpectedOneInstance(BaseAppException):
    as_http = HTTPException(
        status_code=409,
        message="There are duplicates that cannot be processed"
    )


class InstanceNotFound(BaseAppException):
    as_http = HTTPException(
        status_code=404,
        message="Failed to find this object"
    )


class ExpectedUniqueEmail(BaseAppException):
    as_http = HTTPException(
        status_code=400,
        message="This email is already taken"
    )


class ExpectedUniqueLogin(BaseAppException):
    as_http = HTTPException(
        status_code=400,
        message="This username is already taken"
    )
