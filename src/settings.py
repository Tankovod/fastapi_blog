from typing import Any

from jinja2 import pass_context
from starlette.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi_login import LoginManager
from fastapi_pagination.links import Page
from fastapi import Query
from passlib.context import CryptContext
from src.validation.settings import settings


templates = Jinja2Templates(directory="templates")


@pass_context
def https_url_for(context: dict, name: str, **path_params: Any) -> str:

    request = context["request"]
    return request.url_for(name, **path_params).replace("http", "https", 1)


templates.env.globals["url_for"] = https_url_for

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Page = Page.with_custom_options(
    size=Query(3, ge=1, le=300),
)

manager = LoginManager(settings.SECRET_KEY.get_secret_value(), '/login')
