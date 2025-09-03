from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class AppUser(SQLModel, table=True):
    __tablename__ = "app_user"
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
