from mongoengine import (
    Document,
    StringField,
    EmailField, SequenceField,
)
from pydantic import BaseModel


class Account(Document):
    meta = {"collection": "accounts"}
    cId = SequenceField(db_field="c")

    email = EmailField(required=True)
    password = StringField(required=True)


class AccountCreateDTO(BaseModel):
    name: str
    email: str
    password: str


class AccountUpdateDTO(BaseModel):
    name: str | None = None
    email: str | None = None
