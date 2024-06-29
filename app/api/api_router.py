from fastapi import APIRouter

from app.api.routers.auth import auth_router
from app.api.routers.user import user_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(user_router, prefix="/users", tags=["Users"])
