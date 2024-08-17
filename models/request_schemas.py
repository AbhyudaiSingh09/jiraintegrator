from pydantic import BaseModel, field_validator
from requests.auth import HTTPBasicAuth

class RequestBody(BaseModel):
    issue_Key: str
    title: str
    version_number: str
    confluence_page_id: str
    email: str
    api_token: str

# Define a Pydantic model to parse the JSON body
class UpdatedRequestBody(RequestBody):
    incremented_version_number: int
    api_token_v1: str
    api_token_v2: HTTPBasicAuth

    @field_validator('incremented_version_number')
    def check_version_is_int(cls, v):
        if not isinstance(v, int):
            raise ValueError('Incremented version number must be an integer')
        return v

    class Config:
        arbitrary_types_allowed = True  # Allows non-standard Pydantic types like HTTPBasicAuth