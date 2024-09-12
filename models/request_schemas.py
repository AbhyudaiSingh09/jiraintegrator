from pydantic import BaseModel

class RequestBody(BaseModel):
    issue_key: str

