from logger_config import logger as logger
import requests
import json

def confluence_uploader(updated_request_body,data) -> str:
    # Construct the Confluence API URL for updating content using v2 API
    confluence_url = f"https://smw104-jams.atlassian.net/wiki/api/v2/pages/{updated_request_body.confluence_page_id}"
    
    # Set the headers for the request, including the authorization token and content type
    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
    }
    auth = updated_request_body.api_token_v2
    
    # Prepare the data payload for the request
    data = {
        "id": updated_request_body.confluence_page_id,
        "status": "current",
        "title": updated_request_body.title,
        "body": {
            "representation": "storage",
            "value": data,
        },
        "version": {
            "number": updated_request_body.incremented_version_number,  
            "message": "Updated by JiraIntegrator Server"
        },
    }

    # Send a PUT request to update the Confluence page
    response = requests.put(confluence_url,data=json.dumps(data),headers=headers, auth=auth)
    
    # Check if the update was successful
    if response.status_code == 200:
        logger.info("Content uploaded successfully")
        # logger.info(response.json())  # Log the full response for debugging
        return (f"{response.status_code} :{response.text}")
    else:
        # Log an error message if the update failed
        logger.warning(f"Failed to upload content: {response.status_code} - {response.text}")
        return ""
    
