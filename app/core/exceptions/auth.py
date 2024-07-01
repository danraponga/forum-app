class AuthenticationError(Exception):
    pass


class InvalidCredentials(AuthenticationError):
    def __init__(self):
        self.detail = "Invalid credentials"


class NotAuthorized(AuthenticationError):
    def __init__(self):
        self.detail = "Not authorized"


class TokenExpired(AuthenticationError):
    def __init__(self):
        self.detail = "Token has expired"


class InvalidTokenType(AuthenticationError):
    def __init__(self) -> None:
        self.detail = "Invalid token type"
