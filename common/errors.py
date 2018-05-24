"""Errors of HSYOJ."""


class HsyojError(Exception):
    """Base exception of HSYOJ."""
    pass


# Database errors
class DatabaseError(HsyojError):
    """Database exception of HSYOJ."""
    pass


class UserExistError(DatabaseError):
    """User is exist."""
    pass


class UserNotExistError(DatabaseError):
    """User is not exist."""
    pass


class ProblemNotExistError(DatabaseError):
    """Problem is not exist."""
    pass


class RecordNotExistError(DatabaseError):
    """Record is not exist."""
    pass


# Message queue errors
class PluginError(HsyojError):
    """Plugin exception of HSYOJ."""
    pass


class PluginNotFoundError(PluginError):
    """Plugin is not exist."""
    pass
