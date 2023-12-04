from fastapi.routing import APIRouter
from fastapi.responses import ORJSONResponse
from .v1.endpoints import router as v1_router

router = APIRouter(
    default_response_class=ORJSONResponse,
    prefix="/api"
)

router.include_router(v1_router)
