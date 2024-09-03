from pydantic import BaseModel, field_validator
from requests.auth import HTTPBasicAuth

class RequestBody(BaseModel):
    issue_Key: str

# Define a Pydantic model to parse the JSON body
class UpdatedRequestBody(RequestBody):
    api_token_v1: str
    api_token_v2: HTTPBasicAuth


    class Config:
        arbitrary_types_allowed = True  # Allows non-standard Pydantic types like HTTPBasicAuth