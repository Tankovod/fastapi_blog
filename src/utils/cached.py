from fastapi_cache.decorator import cache
from sqlalchemy import select

from src.database.models import Post


@cache(expire=600)
async def get_last_posts(number_of_posts: int) -> list[Post]:
    with Post.session() as session:
        return session.scalars(select(Post).order_by(Post.date_creation).limit(number_of_posts)).all()


