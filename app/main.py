import uvicorn
from fastapi import FastAPI

from app.api.api_router import api_router
from app.core.config import settings

app = FastAPI()
app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
    )
