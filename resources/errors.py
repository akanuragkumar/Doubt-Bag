class InternalServerError(Exception):
    pass


class SchemaValidationError(Exception):
    pass


class ContentAlreadyExistsError(Exception):
    pass


class CreatingContentError(Exception):
    pass


class UpdatingContentError(Exception):
    pass


class DeletingContentError(Exception):
    pass


class ContentNotExistsError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class EmailDoesnotExistsError(Exception):
    pass


class BadTokenError(Exception):
    pass


class ExpiredTokenError(Exception):
    pass

errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    },
    "ContentAlreadyExistsError": {
        "message": "Content with given name already exists",
        "status": 400
    },
    "UpdatingContentError": {
        "message": "Updating content added by other is forbidden",
        "status": 403
    },
    "DeletingContentError": {
        "message": "Deleting content added by other is forbidden",
        "status": 403
    },
    "ContentNotExistsError": {
        "message": "Movie with given id doesn't exists",
        "status": 400
    },
    "EmailAlreadyExistsError": {
        "message": "User with given email address already exists",
        "status": 400
    },
    "UnauthorizedError": {
        "message": "Invalid username or password",
        "status": 401
    },
    "EmailDoesnotExistsError": {
        "message": "Couldn't find the user with given email address",
        "status": 400
    },
    "BadTokenError": {
        "message": "Invalid token",
        "status": 403
    },
    "CreatingContentError": {
        "message": "Creating content added by other is forbidden",
        "status": 403
    },
    "ExpiredTokenError": {
        "message": "The token has already expired",
        "status": 403
    }
}
