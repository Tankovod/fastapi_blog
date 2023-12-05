from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy import Column, VARCHAR, TIMESTAMP, TEXT, ForeignKey
from datetime import datetime


class Post(Base):
    __tablename__ = "post"

    title = Column(VARCHAR(128), unique=True, nullable=False)
    slug = Column(VARCHAR(128), unique=True, nullable=False)
    text = Column(TEXT, unique=False, nullable=False)
    date_creation = Column(TIMESTAMP, nullable=False, default=datetime.now())
    user_id = Column(ForeignKey("site_user.id", ondelete="NO ACTION"), unique=False, nullable=False)
    user = relationship("SiteUser", back_populates="posts")
    image = Column(VARCHAR(256), unique=False, nullable=True, comment="Ссылка на заглавное фото статьи",
                   default="images/hero_1.jpg")
    short_description = Column(VARCHAR(128), unique=False, nullable=True, comment="Краткое описание статьи")
    category_id = Column(ForeignKey("category.id", ondelete="NO ACTION"), unique=False, nullable=False)
    category = relationship("Category", back_populates="posts")
    comments = relationship("Comment")

    def __str__(self):
        return self.slug

    def __repr__(self) -> str:
        return str(self)


class SiteUser(Base):
    __tablename__ = "site_user"
    id = Column(VARCHAR(128), unique=True, nullable=False, primary_key=True)
    first_name = Column(VARCHAR(64), unique=False, nullable=False)
    last_name = Column(VARCHAR(64), unique=False, nullable=True)
    email = Column(VARCHAR(128), unique=True, nullable=False)
    password = Column(VARCHAR(256), unique=False, nullable=False)
    posts = relationship("Post", back_populates="user")
    profile_photo = Column(VARCHAR(256), unique=False, nullable=True, comment="Ссылка на фото пользователя",
                           default="images/blob.svg")
    about = Column(VARCHAR(256), unique=False, nullable=True, comment="Об авторе")

    def __str__(self):
        return f"{self.email} {self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return str(self)


class Comment(Base):
    __tablename__ = "comment"

    name = Column(VARCHAR(32), unique=False, nullable=False)
    text = Column(VARCHAR(64), unique=False, nullable=False)
    date_creation = Column(TIMESTAMP, nullable=False, default=datetime.now())
    email = Column(VARCHAR(128), unique=False, nullable=False)
    post_id = Column(ForeignKey("post.id", ondelete="CASCADE"), nullable=False, unique=False)

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return str(self)


class Category(Base):
    __tablename__ = "category"

    name = Column(VARCHAR(64), unique=True, nullable=False)
    slug = Column(VARCHAR(64), unique=True, nullable=False)
    posts = relationship("Post", back_populates="category")

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return str(self)

