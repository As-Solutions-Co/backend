from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class StudentBase(SQLModel):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    name: str
    birthdate: datetime
    document_number: str
    document_type: str


class Student(StudentBase, table=True): ...
