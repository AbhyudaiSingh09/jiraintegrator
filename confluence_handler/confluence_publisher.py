import requests
from confluence_handler import confluence_pagedata_fetcher, confluence_uploader
from models.confluence_uploader_schema import ConfluencePageResponse
from logger_config import logger


async def create_or_update_confluence_page(
    confluence_config, request_body, page_title, html_content
) -> ConfluencePageResponse:
    # First, check if the page already exists
    page_data = await confluence_pagedata_fetcher.get_page_data(
        confluence_config, page_title
    )

    if page_data:
        logger.info(
            f"Page with title '{page_title}' already exists. Updating the page."
        )
        # If the page exists, update it
        return await confluence_uploader.update_confluence(
            request_body, html_content, confluence_config, page_data
        )

    # If the page does not exist, create a new page
    logger.info(f"Page with title '{page_title}' does not exist. Creating a new page.")
    confluence_page_creator_url = confluence_config.confluence_page_creator_url.format(
        domain=confluence_config.domain_identifier
    )

    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    payload = {
        "spaceId": confluence_config.space_ID,
        "status": "current",
        "title": page_title,
        "parentId": confluence_config.parent_page_ID,
        "body": {"representation": "storage", "value": html_content},
    }

    response = requests.post(
        confluence_page_creator_url,
        json=payload,
        headers=headers,
        auth=confluence_config.api_token_v2,
    )

    if response.status_code == 200:
        response_data = response.json()
        page_id = response_data.get("id")
        version_number = response_data.get("version", {}).get("number", 1)

        page_data = ConfluencePageResponse(
            id=page_id, title=page_title, version=version_number
        )

        logger.info(
            f"The data was uploaded to new Confluence page created with ID: {page_data.id} and Title: {page_data.title}"
        )
        return response.status_code

    else:
        logger.error(f"Failed to create page: {response.status_code} - {response.text}")
        return None
