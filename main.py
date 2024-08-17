from fastapi import FastAPI
from models.request_schemas import RequestBody, UpdatedRequestBody
from utils import increment_version, authentications
from processors import fetch_issue_details,process_download_attachment

app = FastAPI()

@app.post("/download_docx")
async def main(request_body: RequestBody):
    # Access the fields from request_body
    issue_Key = request_body.issue_Key
    title = request_body.title
    version_number = request_body.version_number
    confluence_page_id = request_body.confluence_page_id
    email = request_body.email
    api_token = request_body.api_token

    # Increment the version number
    incremented_version_number = increment_version.increment_version(version_number)

    # Create API tokens
    api_token_v1 = authentications.create_api_token_v1(email, api_token)
    api_token_v2 = authentications.create_api_token_v2(email, api_token)

 # Create a new instance of UpdatedRequestBody
    updated_request_body = UpdatedRequestBody(
        issue_Key=issue_Key,
        title=title,
        version_number=version_number,  # Use the original version number here
        confluence_page_id=confluence_page_id,
        email=email,
        api_token=api_token,
        incremented_version_number=incremented_version_number,
        api_token_v1=api_token_v1,
        api_token_v2=api_token_v2
    )


    issue_details =  fetch_issue_details.fetch_issue_details(updated_request_body)
    download_docx=  process_download_attachment.process_attachments(updated_request_body,issue_details)

    return {"message": "Request Initiated"}