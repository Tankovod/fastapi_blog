from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from sqladmin import Admin
from src.api.router import router as api_router
from src.auth.endpoints import router as auth_router
from src.blog.endpoints import router as views_router
from src.database.admin import SiteUserAdmin, PostAdmin, CommentAdmin, CategoryAdmin  # , AdminAuth
from src.database.base import Base

app = FastAPI()
add_pagination(app)  # добавление пагинации в приложение


app.mount("/static", StaticFiles(directory="static/main"), name="static")
app.mount("/media", StaticFiles(directory="media/main"), name="media")
app.add_middleware(CORSMiddleware,
                   **{'allow_methods': ('*',), 'allow_origins': ('*',),
                      'allow_headers': ('*',), 'allow_credentials': True})
app.include_router(views_router)
app.include_router(auth_router)
app.include_router(api_router)


admin = Admin(app=app, engine=Base.engine)
admin.add_view(SiteUserAdmin)
admin.add_view(CommentAdmin)
admin.add_view(PostAdmin)
admin.add_view(CategoryAdmin)
# admin.add_view(AdminAuth)

