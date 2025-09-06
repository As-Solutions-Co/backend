from sqlmodel import SQLModel


class TokenPayload(SQLModel):
    user_id: str
    organization_id: str
    main_color: str
    exp: int
    iat: int
