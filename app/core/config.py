import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_URI = os.getenv("DB_URI")

    SECRET_KEY = os.getenv("SECRET_KEY")
    HASH_ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 30

    SERVER_HOST = os.getenv("SERVER_HOST")
    SERVER_PORT = int(os.getenv("SERVER_PORT"))


settings = Config()
