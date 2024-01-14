from fastapi import Path
from fastapi.templating import Jinja2Templates
from fastapi_login import LoginManager
from fastapi_pagination.links import Page
from fastapi import Query
from passlib.context import CryptContext
from src.validation.settings import settings

templates = Jinja2Templates(directory="templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Page = Page.with_custom_options(
    size=Query(5, ge=1, le=300),
)

manager = LoginManager(settings.SECRET_KEY.get_secret_value(), '/login')
