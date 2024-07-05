import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_URI = os.getenv("DB_URI")
    TEST_DB_URI = os.getenv("TEST_DB_URI")

    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")

    SECRET_KEY = os.getenv("SECRET_KEY")
    HASH_ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 30

    SERVER_HOST = os.getenv("SERVER_HOST")
    SERVER_PORT = int(os.getenv("SERVER_PORT"))

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    AI_MODEL = "llama3-8b-8192"  # Another models - https://console.groq.com/docs/models
    AI_PROMPT = "You're author of the post with this content: {post}. Consider the following messages from the user as comments to your post."


settings = Config()
