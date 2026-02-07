"""Custom exceptions for the application."""
from fastapi import HTTPException, status


class CredentialsValidationException(HTTPException):
    """
    Represents a user credentials validation error.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )


class IncorrectCredentialException(Exception):
    """
    Represents the error of invalid email and password.
    """

    def __init__(self):
        super().__init__('Incorrect email or password')


class ObjectAlreadyExistException(Exception):
    """
    Represents an error when trying to register a user with the same username.
    """

    def __init__(self, obj_type: str, obj_id: str):
        super().__init__(f'Object {obj_type} already exist with id [{obj_id}]')


class ObjectNotFoundException(Exception):
    """
    Represents an error when the user with a given ID is not found.
    """

    def __init__(self, obj_type: str, obj_id: str):
        super().__init__(f'{obj_type} with ID [{obj_id}] not found')


class ValueRequiredException(Exception):
    """
    Represents an error when a required value is missing.
    """

    def __init__(self, field_name: str):
        super().__init__(f'{field_name} cannot be null')


class IntegrityValidationException(Exception):
    """
    Represents an error when data integrity validation fails.
    """

    def __init__(self, exc_msg: str):
        super().__init__(exc_msg)


class IllegalAccessException(HTTPException):
    """
    Represents an illegal access error.
    """

    def __init__(self, user_id: int, op_code: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'User[{user_id}] not authorized to access Transaction[{op_code}]',
            headers={'WWW-Authenticate': 'Bearer'},
        )


class AmbiguousAuthorizationException(HTTPException):
    """
    Represents an error of ambiguous authorization definition.
    """

    def __init__(self, user_id: int, op_code: str):
        msg = (
            f'Found more than one authorization for User[{user_id}] '
            f'and Transaction[{op_code}]'
        )
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=msg,
            headers={'WWW-Authenticate': 'Bearer'},
        )


class ObjectConflitException(Exception):
    """
    Represents an error when an object conflicts with another existing object.
    """

    def __init__(self, obj_type: str, obj_id: str):
        super().__init__(
            f'{obj_type} with ID [{obj_id}] conflict availability'
        )
