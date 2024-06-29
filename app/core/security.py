from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_token(token_type: str, secret_key: str, expire: datetime, sub: str) -> str:
    to_encode = {"type": token_type, "exp": expire, "sub": sub}
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=settings.HASH_ALGORITHM)
    return encoded_jwt


def create_access_token(user_id: int) -> str:
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_token(
        token_type=ACCESS_TOKEN_TYPE,
        secret_key=settings.SECRET_KEY,
        expire=expire,
        sub=str(user_id),
    )


def create_refresh_token(user_id: int) -> str:
    expire = datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return create_token(
        token_type=REFRESH_TOKEN_TYPE,
        secret_key=settings.SECRET_KEY,
        expire=expire,
        sub=str(user_id),
    )


def decode_token(token: str) -> dict[str, str]:
    decoded_token = jwt.decode(
        token=token, key=settings.SECRET_KEY, algorithms=[settings.HASH_ALGORITHM]
    )
    exp_datetime = datetime.fromtimestamp(decoded_token["exp"], timezone.utc)
    return decoded_token if exp_datetime >= datetime.now(timezone.utc) else None
