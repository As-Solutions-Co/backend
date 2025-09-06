from sqlmodel import Session, select

from app.models.invalid_token_model import InvalidToken


def create_invalid_token(session: Session, token: str) -> InvalidToken:
    new_invalid_token = InvalidToken(token=token)
    session.add(new_invalid_token)
    session.flush()
    session.refresh(new_invalid_token)
    return new_invalid_token


def read_invalid_token(session: Session, token: str) -> InvalidToken | None:
    stmt = select(InvalidToken).where(InvalidToken.token == token)
    return session.exec(stmt).first()
