from sqlmodel import Field, SQLModel

from .mixins import MixinBase


class Country(MixinBase, table=True):
    iso: str = Field(max_length=2, unique=True)
    name: str = Field(unique=True, max_length=100)
    nice_name: str = Field(unique=True, max_length=100)
    iso3: str = Field(unique=True, nullable=True, default=None, max_length=3)
    num_code: int = Field(nullable=True, default=None, max_digits=6)
    phone_code: int = Field(nullable=False, max_digits=5)


class CountriesPublic(SQLModel):
    data: list[Country]
    count: int
