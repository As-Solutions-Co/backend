from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt

from app.core.config import settings
from app.schemas.token_payload import TokenPayload

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    password_bytes = password.encode()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode()


def check_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode()
    hashed_password_bytes = hashed_password.encode()
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)


def generate_token(payload: dict[str, Any]) -> str:
    time_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    created_at = datetime.now(UTC)
    expire = created_at + time_delta
    payload["exp"] = expire
    payload["iat"] = int(created_at.timestamp())
    print(settings.SECRET_KEY)
    return jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm=ALGORITHM)


def check_token(token: str) -> TokenPayload:
    payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=ALGORITHM)
    return TokenPayload(**payload)
