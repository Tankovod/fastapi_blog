from fastapi import status, Request
from src.settings import templates
from .router import router


@router.get("/login", status_code=status.HTTP_200_OK)
async def login(request: Request):
    return templates.TemplateResponse("main/auth/auth.html", {"request": request})




