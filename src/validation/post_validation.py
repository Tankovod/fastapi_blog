from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, model_validator
from slugify import slugify


class GenModel(BaseModel):
    id: PositiveInt

    class Config:
        from_attributes = True


class PostModel(BaseModel):
    title: str = Field(default=..., max_length=128, min_length=1)
    slug: Optional[str] = Field(default="", max_length=128, min_length=1)
    text: str = Field(default=...)
    date_creation: Optional[datetime] = Field(default=datetime.now())
    short_description: str

    @model_validator(mode="after")
    def make_a_slug(self):
        self.slug = slugify(self.title)


class PostDbModel(PostModel, GenModel):
    user_id: PositiveInt
    id: PositiveInt

    def make_a_slug(self):
        pass

