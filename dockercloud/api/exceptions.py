class ApiError(Exception):
    """An error status code was returned when querying the HTTP API"""
    pass


class AuthError(ApiError):
    """An 401 Unauthorized status code was returned when querying the API"""
    pass


class NonUniqueIdentifier(ApiError):
    pass


class ObjectNotFound(ApiError):
    pass
