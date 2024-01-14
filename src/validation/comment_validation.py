from pydantic import BaseModel, Field, PositiveInt
from datetime import datetime


class CommentModel(BaseModel):
    post_id: PositiveInt
    name: str
    text: str
    date_creation: datetime = Field(default=datetime.now())
    email: str
