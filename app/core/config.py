import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_URI = os.getenv("DB_URI")
    TEST_DB_URI = os.getenv("TEST_DB_URI")
    REDIS_URL = os.getenv("REDIS_URL")

    SECRET_KEY = os.getenv("SECRET_KEY")
    HASH_ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 30

    SERVER_HOST = os.getenv("SERVER_HOST")
    SERVER_PORT = int(os.getenv("SERVER_PORT"))

    AI_API_KEY = os.getenv("AI_API_KEY")
    AI_MODEL = "llama3-8b-8192"  # Another models - https://console.groq.com/docs/models
    AI_PROMPT = (
        "Imagine you're author of the post {post}. Some user left a comment on your post: {comment}."
        "You need to response to a comment briefly, taking into account the context of"
        "the post and comment. Be concise and try to match the author of the post."
    )


settings = Config()
