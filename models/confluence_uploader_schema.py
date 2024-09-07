from pydantic import BaseModel,field_validator
from typing import Optional

class PageVersion(BaseModel):
    number: Optional[int]

class ConfluencePageResponse(BaseModel):
    id: int
    title: str
    version: int

