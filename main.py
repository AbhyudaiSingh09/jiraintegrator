from fastapi import FastAPI
from models import request_schemas, envvar_schema
from utils import increment_version, authentications
from processors import fetch_issue_details,process_download_attachment,confluence_uploader
from config.config_loader import yaml_config
from config.env_loader import load_environment_variables


app = FastAPI()


# Load environment variables
load_environment_variables()

# Load environment config using Pydantic
env_config = envvar_schema.load_env_config()

@app.post("/Upload_to_confluence")
async def main(request_body: request_schemas.RequestBody):
    # Access the fields from request_body
    issue_Key = request_body.issue_Key
    title = request_body.title
    version_number = request_body.version_number
    confluence_page_id = request_body.confluence_page_id
    # Increment the version number
    incremented_version_number = increment_version.increment_version(version_number)

    email = env_config.EMAIL
    api_token = env_config.API_TOKEN

    # Create API tokens
    api_token_v1 = authentications.create_api_token_v1(email, api_token)
    api_token_v2 = authentications.create_api_token_v2(email, api_token)

 # Create a new instance of UpdatedRequestBody
    updated_request_body = request_schemas.UpdatedRequestBody(
        issue_Key=issue_Key,
        title=title,
        version_number=version_number, 
        confluence_page_id=confluence_page_id,
        email=email,
        api_token=api_token,
        incremented_version_number=incremented_version_number,
        api_token_v1=api_token_v1,
        api_token_v2=api_token_v2
    )


    issue_details =  await fetch_issue_details.fetch_issue_details(updated_request_body,yaml_config)
    html_content=  await process_download_attachment.process_attachments(updated_request_body,issue_details,yaml_config)
    respone =  await confluence_uploader.confluence_uploader(updated_request_body,html_content,yaml_config)
    return {respone}