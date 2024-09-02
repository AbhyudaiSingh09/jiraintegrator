from pydantic import BaseModel, conlist
from typing import List, Optional

# Define a model for the Confluence configuration
class ConfluenceConfig(BaseModel):
    confluence_uploader_url: str
    jira_issue_url: str
    confluence_page_creator_url: str
    domain_identidfier: str
    space_key: str
    status: str
    representation: str
    message: str
    space_ID: str
    parent_page_ID: str







class ExtensionsConfig(BaseModel):
    extensions: List[str]


# Define a model for the Folder configuration
class FolderConfig(BaseModel):
    temp_folder: str

# Define a model that encapsulates the entire configuration
class AppConfig(BaseModel):
    Confluence: ConfluenceConfig
    Folder: FolderConfig
    Extensions: ExtensionsConfig


