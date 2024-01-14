from .router import router
from src.settings import templates
from fastapi import Request, status


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    name="Резюме Дмитрия"
)
async def dmitry_cv(request: Request):
    return templates.TemplateResponse(name="cv/dmitry.html", context={"request": request, "status": 200})