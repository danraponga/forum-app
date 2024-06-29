from fastapi import Query
from pydantic import BaseModel


class Pagination(BaseModel):
    skip: int = Query(0, ge=0)
    limit: int = Query(10, ge=10)
