class AppException(Exception):
    """
    Base class for all application-specific exceptions.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UserAlreadyExistsError(AppException):
    """
    Raised when a username or email already exists.
    """

    pass


class InvalidCredentialsError(AppException):
    """
    Raised when authentication fails due to invalid credentials.
    """

    pass


class ProblemAlreadyExistsError(AppException):
    """
    Raised when a problem title or slug already exists.
    """

    pass


class ProblemNotFoundError(AppException):
    """
    Raised when a requested problem does not exist.
    """

    pass