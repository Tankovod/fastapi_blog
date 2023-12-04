from typing import Union

from fastapi import Request, status, Form, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.database.models import Post, Comment
from src.dependencies import get_post_info, get_db_session, user_auth, is_user_authorized
from src.settings import templates
from src.validation.comment_validation import CommentModel
from src.validation.post_validation import PostModel
from .router import router
from fastapi_pagination.ext.sqlalchemy import paginate
from src.settings import Page
from ..validation.user_validators import UserView


@router.get(path="/posts", status_code=status.HTTP_200_OK, response_model=Page[Post])
async def get_posts(request: Request, db=get_db_session, user: Union[UserView, int] = is_user_authorized):
    # with Post.session() as session:
    #     posts = session.scalars(select(Post)).all()
    return templates.TemplateResponse("main/posts.html", context={"request": request,
                                                                  "posts": paginate(db, select(Post).order_by(Post.date_creation)),
                                                                  "user": user})


@router.get(path="/", status_code=200)
async def index(request: Request, user: Union[UserView, int] = is_user_authorized):
    with Post.session() as session:
        posts = session.scalars(select(Post).order_by(Post.date_creation).limit(5)).all()
    return templates.TemplateResponse("main/index.html",
                                      context={"request": request, "posts": posts, "user": user})


@router.get(path="/post/{slug}", status_code=status.HTTP_200_OK)
async def get_post_info(request: Request, post: Post = get_post_info, user: Union[UserView, int] = is_user_authorized):
    # print(post.__dict__)
    # print(PostDbModel)
    # t = PostDbModel.model_validate(obj=post, from_attributes=True, strict=True)
    # print(111, t)
    return templates.TemplateResponse("main/post.html",
                                      context={"request": request,
                                               "post": post, "user": user})


@router.post(path="/post/{slug}", status_code=status.HTTP_201_CREATED)
async def leave_comment(request: Request, name=Form(...), email=Form(...), text=Form(...), slug: str = Path(...),
                        user: Union[UserView, int] = is_user_authorized):
    new_comment = CommentModel(name=name, email=email, text=text)
    with Post.session() as session:
        post = session.scalar(select(Post).filter(Post.slug == slug))
        comment = Comment(**new_comment.model_dump(), post_id=post.id)
        session.add(comment)
        session.commit()
        session.refresh(comment)

        return templates.TemplateResponse("main/post.html", context={"request": request, "post": post, "user": user})


@router.get(path="/add-post", status_code=status.HTTP_200_OK)
async def add_post(request: Request, user_or_401: Union[UserView, int] = user_auth):
    return templates.TemplateResponse("main/add-post.html", context={"request": request, "user": user_or_401})


@router.post(path="/add-post", status_code=status.HTTP_201_CREATED)
async def add_new_post(request: Request, title=Form(...), text=Form(...), short_description=Form(...),
                       user_or_401: Union[UserView, int] = user_auth):
    """
    Добавление нового поста
    :param user_or_401: получает текущего пользователя или вызывает ошибку 401
    :param request: данные запроса
    :param title: заголовок поста
    :param text: текст поста
    :param short_description: Краткое описание
    :return: страница добавления поста
    """
    new_post = PostModel(text=text, title=title, short_description=short_description)
    with Post.session() as session:
        post = Post(**new_post.model_dump(), user_id=user_or_401.id)
        print(post.__dict__)
        session.add(post)
        try:
            session.commit()
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Пост с таким заголовком уже существует")
        session.refresh(post)

    return templates.TemplateResponse("main/add-post.html", context={"request": request, "user": user_or_401})


@router.get("/profile", status_code=status.HTTP_200_OK)
async def show_user_profile(request: Request, user_or_401: Union[UserView, int] = user_auth):
    return templates.TemplateResponse("main/profile.html", context={"request": request, "user": user_or_401})

