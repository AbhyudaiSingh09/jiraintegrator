from fastapi import FastAPI, Depends
from confluence_handler import confluence_publisher
from models import request_schemas
from processors import fetch_issue_details, process_download_attachment
from config import ConfluenceConfig
from logger_config import logger as logger

app = FastAPI()


# Dependency to load ConfluenceConfig
def get_confluence_config() -> ConfluenceConfig:
    return ConfluenceConfig()  # Loads the configuration from .env and defaults


@app.post("/upload_to_confluence")
# async def main(request_body: request_schemas.RequestBody):
async def upload_to_confluence(
    request_body: request_schemas.RequestBody,
    confluence_config: ConfluenceConfig = Depends(get_confluence_config),
):
    logger.info(f"Config loaded and Request Initiated for {request_body.issue_key}")

    issue_details = await fetch_issue_details.fetch_issue_details(
        request_body, confluence_config
    )
    html_content, page_title = await process_download_attachment.process_attachments(
        request_body, issue_details, confluence_config
    )
    respone = await confluence_publisher.create_or_update_confluence_page(
        confluence_config, request_body, page_title, html_content
    )
    return {respone}
