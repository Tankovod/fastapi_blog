from .router import router
from src.settings import templates
from fastapi import Request, status
from fastapi.responses import FileResponse


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    name="Резюме Дмитрия"
)
async def dmitry_cv(request: Request):
    return templates.TemplateResponse(name="cv/index.html", context={"request": request, "status": 200})


@router.get(
    "/dmitry-belousov-cv.pdf",
    status_code=status.HTTP_200_OK,
    name="Резюме Дмитрия Pdf"
)
async def dmitry_cv_pdf(request: Request):
    return FileResponse("static/cv/dmitry-belousov-cv.pdf", media_type="application/pdf", headers=request.headers)
