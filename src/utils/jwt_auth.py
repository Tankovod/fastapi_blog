from datetime import datetime, timedelta
from typing import Union

from fastapi import status
from jose import jwt

from src.database.repository import get_user
from src.settings import pwd_context
from src.validation.settings import settings
from src.validation.user_validators import UserView


async def get_password_hash(password):
    return pwd_context.hash(password)


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, password: str):
    user = await get_user(email=email)
    if not user:
        return False
    if not await verify_password(password, user.password):
        return False
    return user


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY.get_secret_value(),
                             algorithm=settings.ALGORITHM)
    access_token = {'access_token': encoded_jwt, 'expire_in': datetime.timestamp(expire)}
    return access_token


async def token_check(token: str) -> UserView:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY.get_secret_value(),
                             algorithms=[settings.ALGORITHM])
    except Exception as ex:
        return status.HTTP_401_UNAUTHORIZED
    user_id = payload.get('sub')
    user = await get_user(user_id=user_id)
    if not user:
        return status.HTTP_401_UNAUTHORIZED
    user = user.__dict__
    user.pop("_sa_instance_state")
    return UserView(**user)


async def get_user_id(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY.get_secret_value(),
                             algorithms=[settings.ALGORITHM.unicode_string()])
    except Exception as ex:
        return status.HTTP_401_UNAUTHORIZED
    return payload.get('sub')
