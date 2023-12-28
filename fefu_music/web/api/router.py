from fastapi.routing import APIRouter

from fefu_music.web.api import albums, auth, landing, monitoring, playlists, tracks

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(auth.router, tags=["auth endpoints"])
api_router.include_router(landing.router, tags=["data for landing"])
api_router.include_router(tracks.router, tags=["track endpoints"])
api_router.include_router(albums.router, tags=["album endpoints"])
api_router.include_router(playlists.router, tags=["playlists endpoints"])
