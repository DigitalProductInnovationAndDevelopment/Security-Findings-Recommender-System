from pydantic import BaseModel


class Pagination(BaseModel):
    offset: int
    limit: int
    total: int
    count: int


class PaginationInput(BaseModel):
    offset: int
    limit: int
