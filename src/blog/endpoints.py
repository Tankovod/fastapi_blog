from typing import Union

from fastapi import Request, status, Form, HTTPException, Path
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import defer

from src.database.models import Post, Comment, Category
from src.dependencies import get_post_info, get_db_session, user_auth, is_user_authorized, get_categories
from src.settings import Page
from src.settings import templates
from src.utils.cached import get_last_posts, get_cached_categories
from src.validation.comment_validation import CommentModel
from src.validation.post_validation import PostModel
from .router import router
from ..validation.user_validators import UserView


@router.get(path="/posts", status_code=status.HTTP_200_OK, response_model=Page[Post])
async def get_posts(request: Request,
                    db=get_db_session,
                    user: Union[UserView, int] = is_user_authorized,
                    categories=get_categories):
    return templates.TemplateResponse("main/posts.html", context={"request": request,
                                                                  "posts": paginate(db, select(Post)
                                                                                    .options(defer(Post.text))
                                                                                    .order_by(Post.date_creation)),
                                                                  "user": user,
                                                                  "categories": await get_cached_categories()})


@router.get(path="/", status_code=200)
async def index(request: Request,
                user: Union[UserView, int] = is_user_authorized,
                categories: list[Category] = get_categories):
    return templates.TemplateResponse("main/index.html",
                                      context={"request": request,
                                               "posts": await get_last_posts(number_of_posts=5),
                                               "user": user,
                                               "categories": categories})


@router.get(path="/posts/{category}/{slug}", status_code=status.HTTP_200_OK)
async def get_post_info(request: Request,
                        post: Post = get_post_info,
                        user: Union[UserView, int] = is_user_authorized,
                        categories: list[str] = get_categories,
                        category: str = Path(...)):
    return templates.TemplateResponse("main/post.html",
                                      context={"request": request,
                                               "post": post, "user": user,
                                               "categories": categories, "category": category})


@router.get("/posts/{category}", status_code=status.HTTP_200_OK, response_model=Page[Post])
async def get_category_posts(request: Request,
                             category: str = Path(...),
                             db=get_db_session,
                             user: Union[UserView, int] = is_user_authorized,
                             categories: list[Category] = get_categories):
    return templates.TemplateResponse("main/posts.html", context={"request": request,
                                                                  "posts": paginate(db, select(Post)
                                                                                    .filter(Post.category_id == select(Category.id)
                                                                                    .options(defer(Post.text))
                                                                                    .filter(Category.slug == category))
                                                                                    .order_by(Post.date_creation)),
                                                                  "user": user,
                                                                  "categories": categories})


@router.get(path="/add-post", status_code=status.HTTP_200_OK)
async def add_post(request: Request,
                   user_or_401: Union[UserView, int] = user_auth,
                   categories: list[str] = get_categories):
    return templates.TemplateResponse("main/add-post.html",
                                      context={"request": request, "user": user_or_401, "categories": categories})


@router.get("/profile", status_code=status.HTTP_200_OK)
async def show_user_profile(request: Request,
                            user_or_401: Union[UserView, int] = user_auth,
                            categories: list[Category] = get_categories):
    return templates.TemplateResponse("main/profile.html",
                                      context={"request": request, "user": user_or_401, "categories": categories})


@router.get("/about", status_code=status.HTTP_200_OK)
async def about_us(request: Request,
                   user: Union[UserView, int] = is_user_authorized,
                   categories: list[Category] = get_categories):
    return templates.TemplateResponse("main/about.html",
                                      context={"request": request, "user": user, "categories": categories})
