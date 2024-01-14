from datetime import timedelta
from typing import Union
from slugify import slugify
from fastapi import status, HTTPException, Form, Path, Request
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.database.models import SiteUser, Post, Comment
from src.database.repository import get_user
from src.utils.jwt_auth import create_access_token, verify_password
from src.utils.jwt_auth import get_password_hash, token_check
from src.validation.auth_validators import LoginData
from src.validation.settings import settings
from src.validation.user_validators import User, UserView
from .router import router
from ...dependencies import is_user_authorized, get_categories, user_auth
from ...validation.comment_validation import CommentModel
from ...validation.post_validation import PostModel


@router.post(path="/registration",
             status_code=status.HTTP_201_CREATED,
             name="New user sign up")
async def sign_up(form: User) -> ORJSONResponse:
    """
    Create new user   in db and get new access token

    :param form: registration user form
    :return: JSON response with user's form and new generated token or exception
    """
    user = SiteUser(**form.model_dump())
    try:
        user.password = await get_password_hash(user.password)
        with SiteUser.session() as session:
            session.add(user)
            session.commit()

    except IntegrityError:
        message = 'Пользователь с таким Email уже существует'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    else:
        message = "Success. Registration completed"
        token = await create_access_token(data={"sub": form.id},
                                          expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    return ORJSONResponse(content={'message': message, 'token': token, **form.model_dump(
        exclude={"password", "disabled"})}, status_code=status.HTTP_201_CREATED)


@router.post(path="/login",
             status_code=status.HTTP_200_OK,
             name="User sign in")
async def sign_in(form: LoginData) -> ORJSONResponse:
    """
    If data in user's form is valid create new access token

    :param form: user's login form
    :return: new generated access token or exception
    """
    current_user = await get_user(email=form.email)
    if current_user and await verify_password(plain_password=form.password, hashed_password=current_user.password):
        token = await create_access_token(data={"sub": current_user.id},
                                          expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        return ORJSONResponse(content={'token': token}, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(detail='Неверный email и (или) пароль', status_code=status.HTTP_400_BAD_REQUEST)


@router.post(path="/token", status_code=status.HTTP_200_OK, name="token validation")
async def validate_token(token: dict) -> None | UserView:
    return await token_check(token=token['access_token'].split('=')[1])


@router.post(path="/posts/{category}/{post}", status_code=status.HTTP_201_CREATED)
async def leave_comment(new_comment: CommentModel):
    with Post.session() as session:
        comment = Comment(**new_comment.model_dump())
        session.add(comment)
        session.commit()
        session.refresh(comment)

    return ORJSONResponse(status_code=status.HTTP_201_CREATED, content=new_comment.model_dump())


@router.post(path="/add-post",
             status_code=status.HTTP_201_CREATED)
async def add_new_post(new_post: PostModel,
                       user_or_401: Union[UserView, int] = user_auth):
    """
    Добавление нового поста
    :param new_post:
    :param user_or_401: получает текущего пользователя или вызывает ошибку 401
    :return: данные нового поста
    """
    print(new_post)
    with Post.session() as session:
        post = Post(**new_post.model_dump(exclude={"slug"}), user_id=user_or_401.id, slug=slugify(new_post.title))
        # print(post.__dict__)
        session.add(post)
        try:
            session.commit()
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Пост с таким заголовком уже существует")
        session.refresh(post)

    return ORJSONResponse(status_code=status.HTTP_201_CREATED, content=new_post.model_dump())

