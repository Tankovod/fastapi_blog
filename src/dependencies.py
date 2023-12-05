from typing import Union

from fastapi import Depends, Path, status, HTTPException, Cookie, Request
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.database.models import Post, Base, Category
from src.utils.jwt_auth import token_check
from src.validation.user_validators import UserView


async def _get_db_session():
    with Base.session() as session:
        yield session


async def _get_post_info(slug: str = Path(default=..., min_length=1, max_length=128,
                                             examples=["big-stick", "lamp"])) -> Post:
    with Post.session() as session:
        post = session.scalar(select(Post).filter(Post.slug == slug).options(joinedload(Post.user), joinedload(Post.comments)))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post was not found")
    return post


async def _user_auth(access_token: str = Cookie(...)) -> Union[UserView, int]:  # для views
    user_or_401 = await token_check(token=access_token)
    if user_or_401 == status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user_or_401


async def _is_user_authorized(request: Request) -> Union[None, UserView]:  # для страниц, которые доступны всем
    if not 'access_token' in request.cookies:
        return status.HTTP_401_UNAUTHORIZED
    return await token_check(token=request.cookies.get('access_token'))


async def _get_categories() -> list[Category]:
    with Category.session() as session:
        return session.scalars(select(Category)).all()


get_post_info = Depends(_get_post_info)
get_db_session = Depends(_get_db_session)
user_auth = Depends(_user_auth)
is_user_authorized = Depends(_is_user_authorized)
get_categories = Depends(_get_categories)
