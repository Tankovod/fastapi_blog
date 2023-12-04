from pydantic import BaseModel, Field


class LoginData(BaseModel):
    email: str = Field(default=...)
    password: str = Field(default=...)
