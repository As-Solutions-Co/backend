from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import SessionDep, TokenDep
from app.models.invalid_token_model import InvalidToken
from app.schemas.auth_schema import RegisterRequest
from app.schemas.token_schema import Token
from app.services.auth_service import login_service, register_service

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register")
def register(session: SessionDep, register_data: RegisterRequest):
    organization, user = register_service(session, register_data)
    return {"organization": organization, "user": user}


@auth_router.post("/login")
def login(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    return login_service(session, form_data)


@auth_router.post("/logout")
def logout(session: SessionDep, token: TokenDep):
    try:
        token_in = InvalidToken(token=token)
        session.add(token_in)
        session.commit()
        session.refresh(token_in)
        return token_in
    except Exception as e:
        print(e)
        session.rollback()
        raise HTTPException(status_code=400)
