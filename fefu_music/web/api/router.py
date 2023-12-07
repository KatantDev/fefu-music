from fastapi.routing import APIRouter

from fefu_music.web.api import auth, landing, monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(auth.router, tags=["auth endpoints"])
api_router.include_router(landing.router, tags=["data for landing"])
