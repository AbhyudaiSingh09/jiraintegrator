from logger_config import logger as logger
import requests 
import json


def fetch_issue_details(updated_request_body):
    # Construct the Jira API URL for fetching issue details
    jira_url = f"https://smw104-jams.atlassian.net/rest/api/3/issue/{updated_request_body.issue_Key}"
    # jira_url=f"https://smw104-jams.atlassian.net/wiki/api/v2/attachments/{issue_key}"
   
    # Set the headers for the request, including the authorization token
    headers = {
        'Authorization': f'Basic {updated_request_body.api_token_v1}',
        'Accept': 'application/json'
    }

    # Send a GET request to fetch the issue details
    try:
        # Attempt to send a GET request to fetch the issue details
        response = requests.get(jira_url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()  # Return the JSON response if successful

    except requests.exceptions.HTTPError as http_err:
        # Log and print the specific HTTP error
        logger.error(f"HTTP error occurred: {http_err}")
        print(f"HTTP error occurred: {http_err}")

    except requests.exceptions.ConnectionError as conn_err:
        # Log and print any connection-related errors
        logger.error(f"Connection error occurred: {conn_err}")
        print(f"Connection error occurred: {conn_err}")

    except requests.exceptions.Timeout as timeout_err:
        # Log and print any timeout errors
        logger.error(f"Timeout error occurred: {timeout_err}")
        print(f"Timeout error occurred: {timeout_err}")

    except requests.exceptions.RequestException as req_err:
        # Catch all other request-related errors
        logger.error(f"An error occurred: {req_err}")
        print(f"An error occurred: {req_err}")

    return ""  # Return "" if any errors occurred