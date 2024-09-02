# To get the details and for future use,not integraget with main 

import requests
import json



def get_details(updated_request_body,yaml_config):
    url = f"https://{yaml_config.Confluence.domain_identidfier}.atlassian.net/wiki/rest/api/space/{yaml_config.Confluence.space_key}"
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, auth=updated_request_body.api_token_v2)
    space_info = response.json()

    print(json.dumps(space_info, indent=4))

    # Extract the spaceId
    space_id = space_info['id']  # or however the id is represented in the response
    print(f"Space ID: {space_id}") 



def get_parentid(updated_request_body,yaml_config):

    parent_page_title = "TEST4"  # Replace with the title of the parent page
    url = f"https://{yaml_config.Confluence.domain_identidfier}.atlassian.net/wiki/rest/api/content?spaceKey={yaml_config.Confluence.space_key}&title={parent_page_title}"


    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, auth=updated_request_body.api_token_v2)
    pages_info = response.json()

    print(json.dumps(pages_info, indent=4))

    # Extract the parentId (the ID of the parent page)
    if pages_info['results']:
        parent_id = pages_info['results'][0]['id']  # Assuming the first result is the correct parent page
        print(f"Parent Page ID: {parent_id}")
    else:
        print("Parent page not found")