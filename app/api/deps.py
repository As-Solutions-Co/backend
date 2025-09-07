from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from app.core.config import settings
from app.core.db import engine
from app.core.security import check_token
from app.crud.app_user_crud import read_app_user_by_id
from app.models.app_user_model import AppUser


def get_db() -> Generator[Session]:
    with Session(engine) as session:
        yield session


oauth_schema = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth_schema)]


def get_current_user(session: SessionDep, token: TokenDep) -> AppUser:
    try:
        payload = check_token(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = read_app_user_by_id(session, payload.user_id)
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUserDep = Annotated[AppUser, Depends(get_current_user)]
