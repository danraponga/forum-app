from fastapi import FastAPI

from app.api.api_router import api_router


def init_routers(app: FastAPI):
    app.include_router(api_router)
