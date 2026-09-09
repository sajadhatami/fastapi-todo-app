







class BaseDomainException(Exception):
    """
    Base exception for all domain logic errors.
    This helps us catch business errors easily in the web layer.
    """
    

class TodoNotFoundException(BaseDomainException):
    """
    Raised when a requested Todo does not exist or does not belong to the user.
    """
    