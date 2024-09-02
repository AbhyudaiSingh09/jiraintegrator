from logger_config import logger as logger
import requests 



async def fetch_issue_details(updated_request_body,yaml_config):
    
    # Construct the Jira API URL for fetching issue details
    jira_url = yaml_config.Confluence.jira_issue_url.format(issue_Key=updated_request_body.issue_Key,domain=yaml_config.Confluence.domain_identidfier)

    # Set the headers for the request, including the authorization token
    headers = {
        'Authorization': f'Basic {updated_request_body.api_token_v1}',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(jira_url, headers=headers)
        response.raise_for_status()  
        return response.json()  

    except requests.exceptions.HTTPError as http_err:
        # Log and print the specific HTTP error
        logger.error(f"HTTP error occurred: {http_err}")

    except requests.exceptions.ConnectionError as conn_err:
        # Log and print any connection-related errors
        logger.error(f"Connection error occurred: {conn_err}")


    except requests.exceptions.Timeout as timeout_err:
        # Log and print any timeout errors
        logger.error(f"Timeout error occurred: {timeout_err}")


    except requests.exceptions.RequestException as req_err:
        # Catch all other request-related errors
        logger.error(f"An error occurred: {req_err}")


    return ""  