from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.orm import selectinload, defer, load_only

from src.database.models import Post, Category


@cache(expire=600)
async def get_last_posts(number_of_posts: int) -> list[Post]:
    with Post.session() as session:
        posts = session.scalars(select(Post)
                                .options(selectinload(Post.category),
                                         defer(Post.text))  # defer = не выбираем столбец text
                                .order_by(Post.date_creation)
                                .limit(number_of_posts)).all()
        for post in posts:  # используем strftime, т. к. redis преобразует в строку
            post.date_creation = post.date_creation.strftime("%d %B, %Y")
        return posts


@cache(expire=600)
async def get_cached_categories() -> list[Category]:
    with Category.session() as session:
        return session.scalars(select(Category)
                               .options(selectinload(Category.posts)
                                        .options(load_only(Post.id)))).all()  # load_only = выбираем определенные столбцы
