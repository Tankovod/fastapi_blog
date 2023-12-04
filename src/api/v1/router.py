from fastapi.routing import APIRouter
from fastapi.responses import ORJSONResponse

router = APIRouter(
    default_response_class=ORJSONResponse,
    prefix="/v1"
)
