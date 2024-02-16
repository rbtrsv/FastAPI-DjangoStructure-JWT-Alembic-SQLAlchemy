from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from core.config import settings

from apps.main.router import router as main_router
from apps.songs.router import router as songs_router
from apps.custom_auth.routers.users_router import router as users_router
# from apps.another_auth.routers.auth import router as auth_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(main_router, prefix="", tags=["Main"])
app.include_router(songs_router, prefix="/songs", tags=["Songs"])
app.include_router(users_router, prefix="/auth", tags=["Auth"])

