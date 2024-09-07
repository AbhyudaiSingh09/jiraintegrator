import requests
from logger_config import logger
from models.confluence_uploader_schema import ConfluencePageResponse

async def update_confluence(updated_request_body, html_content, yaml_config, page_data: ConfluencePageResponse) -> str:
    confluence_url = yaml_config.Confluence.confluence_uploader_url.format(
        confluence_page_id=page_data.id, 
        domain=yaml_config.Confluence.domain_identidfier
    )

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Prepare the payload for updating the page
    payload = {
        "id": page_data.id,
        "status": yaml_config.Confluence.status,
        "title": page_data.title,
        "body": {
            "representation": yaml_config.Confluence.representation,
            "value": html_content,
        },
        "version": {
            "number": page_data.version,
            "message": yaml_config.Confluence.message
        }
    }


    response = requests.put(
        confluence_url,
        json=payload,
        headers=headers,
        auth=(updated_request_body.api_token_v2)
    )

    if response.status_code == 200:
        logger.info(f"Page with ID '{page_data.id}' updated successfully.")
        return "Success"
    else:
        logger.error(f"Failed to update page: {response.status_code} - {response.text}")
        return "Failure"