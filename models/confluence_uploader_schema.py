from pydantic import BaseModel

class ConfluencePageResponse(BaseModel):
    id: int
    title: str
    version: int

