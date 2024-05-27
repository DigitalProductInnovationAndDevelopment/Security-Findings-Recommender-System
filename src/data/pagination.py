from pydantic import BaseModel

class Pagination(BaseModel):
    offset: int
    limit: int
    total: int
    
    
class PaginationInput(BaseModel):
    offset: int
    limit: int