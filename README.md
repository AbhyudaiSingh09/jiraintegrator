
# Jira Integrator

## Overview

The Jira Integrator is a Python-based tool designed to interact with Jira and Confluence APIs. It allows you to manage Jira issues, upload attachments, and update Confluence pages. The project leverages FastAPI for web framework functionality, handling tasks such as incrementing version numbers, processing `.docx` files, and converting them to Markdown format.

## Features

- **Fetch Jira Issue Details**: Retrieve and process detailed information about Jira issues.
- **Version Management**: Automatically increment version numbers in Jira issues.
- **Document Processing**: Convert `.docx` files to Markdown format and process them.
- **Confluence Integration**: Upload images and update Confluence pages with new content.

## Prerequisites

- Python 3.8 or later
- Jira and Confluence accounts with API tokens

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/jira_integrator.git
cd jira_integrator
```

## Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
## Install Dependencies
```bash
pip install -r requirements.txt
```

## Configuration
Before running the application, ensure that you have set up the necessary environment variables:

	•	JIRA_API_TOKEN: Your Jira API token.
	•	CONFLUENCE_API_TOKEN: Your Confluence API token.
	•	JIRA_BASE_URL: The base URL of your Jira instance.
	•	CONFLUENCE_BASE_URL: The base URL of your Confluence instance.


## Usage
	•	Running the FastAPI Server
	•	Start the FastAPI server by running:
```bash
uvicorn main:app --reload
```
	•	This will launch the server at http://127.0.0.1:8000.

## Example API Endpoints
	•	Fetch Jira Issue Details:
	•	Send a POST request to /download_docx with a JSON body containing the issue key, email, API token, and other     required fields.
	•	Convert .docx to Markdown:
	•	Automatically converts the .docx file attached to a Jira issue to Markdown and processes it accordingly.

## Development
Code Structure

	•	main.py: The main entry point of the FastAPI application.
	•	models/request_schemas.py: Contains Pydantic models for request and response validation.
	•	utils/increment_version.py: Contains the increment_version function for managing version numbers.


## License
This project is licensed under the MIT License. See the LICENSE file for details.
