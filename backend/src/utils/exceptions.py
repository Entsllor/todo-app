import http

STATUS_DESCRIPTIONS = {i_status.value: i_status.description for i_status in list(http.HTTPStatus)}
DEFAULT_HTTP_ERROR_MESSAGE = "Internal Server Error. Please report this error admin@example.com"
STATUS_DESCRIPTIONS[500] = DEFAULT_HTTP_ERROR_MESSAGE  # override 500 error description


class BaseAppException(Exception):
    message: str = ""

    def __init__(self, message: str = ""):
        if message:
            self.message = message


def handle_app_exception(exception: BaseAppException):
    status_code = getattr(exception, 'http_status_code', 500)
    message = getattr(exception, 'message', STATUS_DESCRIPTIONS.get(status_code, DEFAULT_HTTP_ERROR_MESSAGE))
    return {"error_code": status_code, "error_description": message}, status_code


class IncorrectLoginOrPassword(BaseAppException):
    message = "Incorrect username or password"
    http_status_code = 401


class AccessTokenRequiredError(BaseAppException):
    message = "Excepted a JWT access token"
    http_status_code = 401


class CredentialsException(BaseAppException):
    message = "Could not validate credentials"
    http_status_code = 401


class InactiveUser(BaseAppException):
    message = "Current user is inactive"
    http_status_code = 401


class UserNotFoundError(BaseAppException):
    message = "Failed to find this User"
    http_status_code = 401


class Forbidden(BaseAppException):
    message = "Sorry, but you do not have enough rights"
    http_status_code = 403


class ExpectedOneInstance(BaseAppException):
    message = "There are duplicates that cannot be processed"
    http_status_code = 400


class InstanceNotFound(BaseAppException):
    message = "Failed to find this object"
    http_status_code = 404


class ExpectedUniqueEmail(BaseAppException):
    message = "This email is already taken"
    http_status_code = 400


class ExpectedUniqueLogin(BaseAppException):
    message = "This username is already taken"
    http_status_code = 400
