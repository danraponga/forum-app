from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.services.scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()
