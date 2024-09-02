import requests
import json


def create_confluence_page(yaml_config,updated_request_body):

    confluence_page_creator_url = yaml_config.Confluence.confluence_page_creator_url.format(domain=yaml_config.Confluence.domain_identidfier)

    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

    payload = json.dumps( {
    "spaceId": yaml_config.Confluence.space_ID,
    "status": "current",
    "title": "test6",
    "parentId": yaml_config.Confluence.parent_page_ID,
    "body": {
        "representation": "storage",
        "value": "test"
    }
    } )

    response = requests.request(
    "POST",
    confluence_page_creator_url,
    data=payload,
    headers=headers,
    auth=updated_request_body.api_token_v2
    )

    
    
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))