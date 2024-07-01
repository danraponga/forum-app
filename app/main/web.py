import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.main.exc_handlers import init_exception_handlers
from app.main.routers import init_routers


def create_app() -> FastAPI:
    app = FastAPI()
    init_routers(app)
    init_exception_handlers(app)
    return app


if __name__ == "__main__":
    uvicorn.run(
        "app.main.web:create_app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
        factory=True,
    )
