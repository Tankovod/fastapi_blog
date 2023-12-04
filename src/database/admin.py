from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
from src.database.models import Post, SiteUser, Comment


class PostAdmin(ModelView, model=Post):
    column_list = ["title", "text", "date_creation"]


class SiteUserAdmin(ModelView, model=SiteUser):
    column_list = ["first_name", "last_name", "email"]


class CommentAdmin(ModelView, model=Comment):
    column_list = ["name", "email"]


# class AdminAuth(AuthenticationBackend):
#     async def login(self, request: Request) -> bool:
#         form = await request.form()
#         username, password = form["username"], form["password"]
#         valid_usernames = ["admin"]
#         valid_passwords = ["fb_Admin"]
#         # Validate username/password credentials
#         # And update session
#         if username in valid_usernames and password in valid_passwords:
#             return True
#         return False
#
#     async def logout(self, request: Request) -> bool:
#         # Usually you'd want to just clear the session
#         request.session.clear()
#         return True
#
#     async def authenticate(self, request: Request) -> bool:
#         token = request.session.get("token")
#
#         if not token:
#             return False
#
#         # Check the token in depth
#         return True

