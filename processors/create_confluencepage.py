import requests
import json
from logger_config import logger as logger
from models.confluence_uploader_schema import ConfluencePageResponse
from utils import increment_version


def create_confluence_page(yaml_config, updated_request_body,page_title) -> ConfluencePageResponse:
    print(f"page_title inside:{page_title}")
    confluence_page_creator_url = yaml_config.Confluence.confluence_page_creator_url.format(domain=yaml_config.Confluence.domain_identidfier)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "spaceId": yaml_config.Confluence.space_ID,
        "status": "current",
        "title": page_title,
        "parentId": yaml_config.Confluence.parent_page_ID,
        "body": {
            "representation": "storage",
            "value": "test"
        }
    })

    logger.info("sending request for creating confluence page ..")
    
    response = requests.post(
        confluence_page_creator_url,
        data=payload,
        headers=headers,
        auth=updated_request_body.api_token_v2
    )

    if response.status_code == 200:
        response_data = response.json()
        page_id = response_data.get("id")
        page_title = response_data.get("title")
        version_number = response_data.get("version", {}).get("number", 1) 
        print(f"beforeince:{version_number}")
        version_number = increment_version.increment_version(version_number)
        print(f"afterince:{version_number}")
        page_data = ConfluencePageResponse(
            id=page_id,
            title=page_title,
            version=version_number
        )


        logger.info(f"The confluecne page has been created with id: {page_data.id}, title:{page_data.title} and verson number: {page_data.version}")
        return page_data
    else:
        logger.error(f"Failed to create page: {response.status_code} - {response.text}")
        return ""