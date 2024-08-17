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
    response = requests.get(jira_url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()

        # Pretty-print the JSON with an indentation of 4 spaces
        pretty_json = json.dumps(response_data, indent=4)

        print(pretty_json)
        return response.json()
    else:
        # Log an error message if the request failed
        logger.error(f"Failed to fetch issue details: {response.status_code} - {response.text}")
        return None