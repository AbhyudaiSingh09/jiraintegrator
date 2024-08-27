from pydantic import BaseModel

class RequestBody(BaseModel):
   filename: str
   file_content: str
   file_type: str