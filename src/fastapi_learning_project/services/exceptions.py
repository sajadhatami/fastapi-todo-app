class BaseDomainException(Exception):
    """
    Base exception for all domain logic errors.
    This helps us catch business errors easily in the web layer.
    """


class TodoNotFoundException(BaseDomainException):
    """
    Raised when a requested Todo does not exist or does not belong to the user.
    """


class UserAlreadyExistsException(BaseDomainException):
    """
    Raised when a user with the given email already exists.
    """


class UserNotFoundException(BaseDomainException):
    """
    Raised when a requested User does not exist.
    """


class InvalidCredentialsException(BaseDomainException):
    """
    Raised when authentication fails due to incorrect credentials or inactive state.
    """