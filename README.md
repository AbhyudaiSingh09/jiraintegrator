
# Jira Integrator

## Overview

The Jira Integrator is a Python-based tool designed to interact with Jira and Confluence APIs. It allows you to manage Jira issues, upload attachments, and update Confluence pages. The project leverages FastAPI as the web framework, handling tasks such as incrementing version numbers, processing `.docx` files, converting them to HTML format, and uploading them to Confluence.

## Features

- **Fetch Jira Issue Details**: Retrieve and process detailed information about Jira issues.
- **Version Management**: Automatically increment version numbers in Jira issues.
- **Document Processing**: Convert `.docx` files to HTML format and process them.
- **Confluence Integration**: Upload images and update Confluence pages with new HTML content.

## Prerequisites

- Python 3.8 or later
- Jira and Confluence accounts with API tokens

## Installation

### Clone the Repository

```bash
git clone https://github.com/axs7941onemindservices/JIraIntegrator.git
cd jira_integrator
```

### Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

Before running the application, ensure that you have set up the necessary environment variables:

- **JIRA_API_TOKEN**: Your Jira API token.
- **CONFLUENCE_API_TOKEN**: Your Confluence API token.
- **JIRA_BASE_URL**: The base URL of your Jira instance.
- **CONFLUENCE_BASE_URL**: The base URL of your Confluence instance.

## Usage

### Running the FastAPI Server

Start the FastAPI server by running:

```bash
uvicorn main:app --reload
```

This will launch the server at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Example API Endpoints

#### Upload to Confluence

Send a POST request to `/Upload_to_confluence` with a JSON body containing the required fields.

**Request Body Structure**:

```json
{
    "issue_key": "ISSUE-123",

}
```

**Explanation of Fields**:

- **issue_key**: The Jira issue key associated with the document.
- **title**: The title of the document.
- **version_number**: The current version number of the document.
- **confluence_page_id**: The ID of the Confluence page where the content will be uploaded.
- **email**: The user's email associated with Jira and Confluence.
- **api_token**: The API token for authenticating with Jira and Confluence.

**Description**:

- The API will increment the version number.
- It will then fetch the issue details from Jira.
- The `.docx` file attached to the Jira issue will be processed, converted to HTML format, and uploaded to the specified Confluence page.

### Development

#### Code Structure

- **`main.py`**: The main entry point of the FastAPI application.
- **`models/request_schemas.py`**: Contains Pydantic models for request and response validation.
- **`utils/increment_version.py`**: Contains the `increment_version` function for managing version numbers.
- **`processors/fetch_issue_details.py`**: Handles fetching Jira issue details.
- **`processors/process_download_attachment.py`**: Processes and converts `.docx` attachments to HTML.
- **`processors/confluence_uploader.py`**: Manages uploading HTML content to Confluence.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
