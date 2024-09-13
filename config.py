import base64
from requests.auth import HTTPBasicAuth
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pydantic import AnyHttpUrl


class ConfluenceConfig(BaseSettings):
    confluence_uploader_url: str = (
        "https://{domain}/wiki/api/v2/pages/{confluence_page_id}"
    )
    jira_issue_url: str = "https://{domain}/rest/api/3/issue/{issue_key}"
    confluence_page_creator_url: str = "https://{domain}/wiki/api/v2/pages"
    page_data_url: str = "https://{domain}/wiki/rest/api/content?title={page_title}&spaceKey={space_key}&expand=version"
    domain_identifier: str = "smw104-jams.atlassian.net"
    space_key: str = "Jams104"
    status: str = "current"
    representation: str = "storage"
    message: str = "Updated by JiraIntegrator"
    space_ID: str = "6619140"
    parent_page_ID: str = "7634945"
    working_directory: str = "working_directory/"
    extensions: List[str] = ["md", "html", "docx"]
    EMAIL: str
    API_TOKEN: str
    model_config = SettingsConfigDict(
        env_file=".env"
    )  # Points to .env file for sensitive info

    @classmethod
    def parse_extensions(cls, extensions: str) -> List[str]:
        """Parse comma-separated extensions string from environment variable if provided."""
        return extensions.split(",")

    # Remove __init__ method and handle extension parsing inside the property directly
    @property
    def parsed_extensions(self) -> List[str]:
        """Return parsed extensions from the config or use the default value."""
        return self.parse_extensions(",".join(self.extensions))

    @property
    def api_token_v1(self) -> str:
        """Generate Base64-encoded API token (v1)."""
        return base64.b64encode(f"{self.EMAIL}:{self.API_TOKEN}".encode()).decode(
            "utf-8"
        )

    @property
    def api_token_v2(self) -> HTTPBasicAuth:
        """Generate HTTP Basic Auth token (v2)."""
        return HTTPBasicAuth(self.EMAIL, self.API_TOKEN)
