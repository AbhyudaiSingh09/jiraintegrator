import requests
from logger_config import logger
from models.confluence_uploader_schema import ConfluencePageResponse

async def update_confluence(request_body, html_content, confluence_config, page_data: ConfluencePageResponse) -> str:
    confluence_url = confluence_config.confluence_uploader_url.format(
        confluence_page_id=page_data.id, 
        domain=confluence_config.domain_identifier
    )

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Prepare the payload for updating the page
    payload = {
        "id": page_data.id,
        "status": confluence_config.status,
        "title": page_data.title,
        "body": {
            "representation": confluence_config.representation,
            "value": html_content,
        },
        "version": {
            "number": page_data.version,
            "message": confluence_config.message
        }
    }


    response = requests.put(
        confluence_url,
        json=payload,
        headers=headers,
        auth=(confluence_config.api_token_v2)
    )

    if response.status_code == 200:
        logger.info(f"Page with ID '{page_data.id}' updated successfully.")
        return "Success"
    else:
        logger.error(f"Failed to update page: {response.status_code} - {response.text}")
        return "Failure"