class CPArenaException(Exception):
    """
    Base exception for all application-specific exceptions.
    """

    pass


class AuthenticationError(CPArenaException):
    """
    Raised when authentication fails.
    """

    pass


class InvalidCredentialsError(AuthenticationError):
    """
    Raised when login credentials are invalid.
    """

    pass


class AuthorizationError(CPArenaException):
    """
    Raised when a user is not authorized.
    """

    pass


class UserAlreadyExistsError(CPArenaException):
    """
    Raised when a user already exists.
    """

    pass


class UserNotFoundError(CPArenaException):
    """
    Raised when a user cannot be found.
    """

    pass


class ProblemAlreadyExistsError(CPArenaException):
    """
    Raised when a problem already exists.
    """

    pass


class ProblemNotFoundError(CPArenaException):
    """
    Raised when a problem cannot be found.
    """

    pass


class SubmissionNotFoundError(CPArenaException):
    """
    Raised when a submission cannot be found.
    """

    pass