class AccessDenied(Exception):
    def __init__(self):
        self.detail = "Access denied"


class ProfanityContent(Exception):
    def __init__(self):
        self.detail = "Content contains profanity"
