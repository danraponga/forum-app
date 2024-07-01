class EntityNotFoundError(Exception):
    pass


class PostNotFound(EntityNotFoundError):
    def __init__(self, detail: str = "Post not found"):
        self.detail = detail


class CommentNotFound(EntityNotFoundError):
    def __init__(self, detail: str = "Comment not found"):
        self.detail = detail


class UserNotFound(EntityNotFoundError):
    def __init__(self, detail: str = "User not found"):
        self.detail = detail


class UserAlreadyExists(Exception):
    def __init__(self, detail: str = "User already exists"):
        self.detail = detail
