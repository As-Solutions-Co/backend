from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.schemas.token_payload import TokenPayload

ALGORITHM = "HS256"


pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd.verify(plain_password, hashed_password)


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
