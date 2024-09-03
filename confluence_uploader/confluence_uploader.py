from logger_config import logger as logger
import requests
import json



async def confluence_uploader(updated_request_body,data,yaml_config,page_data) -> str:

    # Construct the Confluence API URL for updating content using v2 API
    confluence_url = yaml_config.Confluence.confluence_uploader_url.format(confluence_page_id=page_data.id, domain=yaml_config.Confluence.domain_identidfier)

    # Set the headers 
    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

    auth = updated_request_body.api_token_v2
    
    # Prepare the data payload for the request
    data = {
        "id": page_data.id,
        "status": yaml_config.Confluence.status,
        "title": page_data.title,
        "body": {
            "representation": yaml_config.Confluence.representation,
            "value": data,
        },
        "version": {
            "number": page_data.version,   
            "message": yaml_config.Confluence.message
        },
    }
    
    # Send a PUT request to update the Confluence page
    response = requests.put(confluence_url,data=json.dumps(data),headers=headers, auth=auth)
    
    # Check if the update was successful
    if response.status_code == 200:
        logger.info("Content uploaded successfully")
        return (response.status_code)
    else:
        # Log an error message if the update failed
        logger.error(f"Failed to upload content: {response.status_code}:{response.text}")
        return (response.status_code)
    
