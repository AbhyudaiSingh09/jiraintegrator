# To get the details and for future use,not integraget with main

import requests
import json


def get_details(request_body, confluence_config):
    url = f"https://{confluence_config.Confluence.domain_identifier}.atlassian.net/wiki/rest/api/space/{confluence_config.Confluence.space_key}"
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=confluence_config.api_token_v2)
    space_info = response.json()

    print(json.dumps(space_info, indent=4))

    # Extract the spaceId
    space_id = space_info["id"]  # or however the id is represented in the response
    print(f"Space ID: {space_id}")


def get_parentid(request_body, confluence_config):
    parent_page_title = "TEST4"  # Replace with the title of the parent page
    url = f"https://{confluence_config.Confluence.domain_identifier}.atlassian.net/wiki/rest/api/content?spaceKey={confluence_config.Confluence.space_key}&title={parent_page_title}"

    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=confluence_config.api_token_v2)
    pages_info = response.json()

    print(json.dumps(pages_info, indent=4))

    # Extract the parentId (the ID of the parent page)
    if pages_info["results"]:
        parent_id = pages_info["results"][0][
            "id"
        ]  # Assuming the first result is the correct parent page
        print(f"Parent Page ID: {parent_id}")
    else:
        print("Parent page not found")
