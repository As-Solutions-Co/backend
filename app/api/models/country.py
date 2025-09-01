from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID


class Country(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4, nullable=False)
    iso: str = Field(max_length=2, unique=True, nullable=False)
    name: str = Field(unique=True, nullable=False, max_length=100)
    nice_name: str = Field(unique=True, nullable=False, max_length=100)
    iso3: str = Field(unique=True, nullable=True, default=None, max_length=3)
    num_code: int = Field(unique=True, nullable=True, default=None, max_digits=6)
    phone_code: int = Field(unique=True, nullable=False, max_digits=5)


class CountriesPublic(SQLModel):
    data: list[Country]
    count: int
