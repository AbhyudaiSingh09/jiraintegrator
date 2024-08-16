from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model to parse the JSON body
class RequestBody(BaseModel):
    issue_Key: str
    title: str
    version_number: str
    confluence_page_id: str
    email: str
    api_token: str

@app.post("/download_docx")
async def read_request(body: RequestBody):
    # Print the received JSON data to the console
    print(body.dict())

    # Return a response (you can modify this as needed)
    return {"message": "Data received", "data": body.dict()}