from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.services.common.scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()
