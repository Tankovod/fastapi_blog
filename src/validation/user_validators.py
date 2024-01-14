import ulid
from pydantic import BaseModel, EmailStr, Field
from .custom_validators import PasswordStr


class User(BaseModel):
    id: str = Field(default_factory=lambda: ulid.ulid(), min_length=26, max_length=26)
    email: EmailStr
    first_name: str = Field(default=..., max_length=32, min_length=2)
    last_name: str = Field(default=..., max_length=32, min_length=2)
    password: PasswordStr = Field(
        default=...,
        min_length=8,
        max_length=64
    )
    about: str = Field(default="-", max_length=128)
    # disabled: bool = False

    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str


class UserView(User):
    id: str = Field(..., min_length=26, max_length=26)

