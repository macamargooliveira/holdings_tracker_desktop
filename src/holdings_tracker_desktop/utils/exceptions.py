class AppException(Exception):
    """Base exception for the application"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class NotFoundException(AppException):
    """Raised when a resource is not found"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message)

class ConflictException(AppException):
    """Raised when there's a conflict (e.g., duplicate)"""
    def __init__(self, message: str = "Conflict occurred"):
        super().__init__(message)

class ValidationException(AppException):
    """Raised when validation fails"""
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message)

class DatabaseException(AppException):
    """Raised when a database error occurs"""
    def __init__(self, message: str = "Database error"):
        super().__init__(message)
