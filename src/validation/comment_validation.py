from pydantic import BaseModel, Field
from datetime import datetime


class CommentModel(BaseModel):
    name: str
    text: str
    date_creation: datetime = Field(default=datetime.now())
    email: str
