from enum import Enum


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"

    def __eq__(self, other):
        if isinstance(other, TokenType):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other
        return False
