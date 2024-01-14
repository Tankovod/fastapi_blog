from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_pagination import add_pagination
from redis import asyncio as aioredis
from sqladmin import Admin
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from src.api.router import router as api_router
from src.auth.endpoints import router as auth_router
from src.blog.endpoints import router as views_router
from src.cv.endpoints import router as cv_router
from src.database.admin import SiteUserAdmin, PostAdmin, CommentAdmin, CategoryAdmin  # , AdminAuth
from src.database.base import Base
from src.validation.settings import settings

app = FastAPI()
add_pagination(parent=app)  # добавление пагинации в приложение


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(settings.REDIS_URL.unicode_string(), encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

app.add_middleware(middleware_class=CORSMiddleware,
                   **{'allow_methods': ('*',), 'allow_origins': ('*',),
                      'allow_headers': ('*',), 'allow_credentials': True})
app.add_middleware(middleware_class=ProxyHeadersMiddleware,
                   trusted_hosts=("*", ))

app.mount("/static", StaticFiles(directory="static/main"), name="static")
app.mount("/cv-static", StaticFiles(directory="static/cv"), name="cv-static")
app.mount("/media", StaticFiles(directory="media/main"), name="media")

app.include_router(router=views_router)
app.include_router(router=auth_router)
app.include_router(router=api_router)
app.include_router(router=cv_router)


admin = Admin(app=app, engine=Base.engine)
admin.add_view(view=SiteUserAdmin)
admin.add_view(view=CommentAdmin)
admin.add_view(view=PostAdmin)
admin.add_view(view=CategoryAdmin)
# admin.add_view(AdminAuth)

