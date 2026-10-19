"""
Domain-specific exceptions for ProductGuard AI.
"""

class ProductGuardException(Exception):
    """Base exception for all ProductGuard AI errors."""
    pass

class ProductNotFoundError(ProductGuardException):
    """Raised when a specified product is not found in the catalog."""
    pass

class CallNotFoundError(ProductGuardException):
    """Raised when a requested call recording or transcript cannot be found."""
    pass

class UnauthorizedAccessError(ProductGuardException):
    """Raised when access to private reports or recordings is forbidden."""
    pass

class DisclosureMissingError(ProductGuardException):
    """Raised when an audio recording lacks participant consent/disclosure."""
    pass

class ParsingError(ProductGuardException):
    """Raised when transcript or audio file ingestion fails."""
    pass
