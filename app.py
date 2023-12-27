from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_pagination import add_pagination
from sqladmin import Admin
from src.api.router import router as api_router
from src.auth.endpoints import router as auth_router
from src.blog.endpoints import router as views_router
from src.database.admin import SiteUserAdmin, PostAdmin, CommentAdmin, CategoryAdmin  # , AdminAuth
from src.database.base import Base
from redis import asyncio as aioredis
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from src.validation.settings import settings

app = FastAPI()
add_pagination(app)  # добавление пагинации в приложение


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(settings.REDIS_URL.unicode_string(), encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

app.mount("/static", StaticFiles(directory="static/main"), name="static")
app.mount("/media", StaticFiles(directory="media/main"), name="media")

app.add_middleware(CORSMiddleware,
                   **{'allow_methods': ('*',), 'allow_origins': ('*',),
                      'allow_headers': ('*',), 'allow_credentials': True})
app.add_middleware(ProxyHeadersMiddleware,
                   trusted_hosts=("*", ))

app.include_router(views_router)
app.include_router(auth_router)
app.include_router(api_router)


admin = Admin(app=app, engine=Base.engine)
admin.add_view(SiteUserAdmin)
admin.add_view(CommentAdmin)
admin.add_view(PostAdmin)
admin.add_view(CategoryAdmin)
# admin.add_view(AdminAuth)

