from better_profanity import profanity


def contains_profanity(content: str) -> bool:
    return profanity.contains_profanity(content)
