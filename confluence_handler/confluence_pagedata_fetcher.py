import requests
from logger_config import logger
from models.confluence_uploader_schema import ConfluencePageResponse
from utils import increment_version

async def get_page_data(confluence_config, page_title) -> ConfluencePageResponse:
    confluence_url = confluence_config.page_data_url.format(
        domain=confluence_config.domain_identifier,
        page_title=page_title,
        space_key=confluence_config.space_key
    )

    headers = {
        "Accept": "application/json"
    }

    logger.info("Fetching page data from Confluence.")

   
    response = requests.get(
        confluence_url,
        headers=headers,
        auth=confluence_config.api_token_v2
    )

    if response.status_code == 200:
        response_data = response.json()

        if response_data.get("results"):
            page = response_data["results"][0]
            page_id = page["id"]
            version_number = page["version"]["number"]
            version_number = increment_version.increment_version(version_number)


            page_data = ConfluencePageResponse(
                id=page_id,
                title=page_title,
                version=version_number
            )

            logger.info(f"Page data retrieved: ID = {page_data.id}, Title = {page_data.title}, Version = {page_data.version}")
            return page_data
        else:
            logger.info(f"No page found with title '{page_title}'.")
            return None
    else:
        logger.error(f"Failed to fetch page data: {response.status_code} - {response.text}")
        return None