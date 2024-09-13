# Jira Integrator

## Overview

The **Jira Integrator** is a Python-based tool designed to interact with Jira and Confluence APIs. It allows users to manage Jira issues, upload attachments, and update Confluence pages. This project leverages **FastAPI** as the web framework, handling tasks such as incrementing version numbers, processing `.docx` files, converting them to HTML format, and uploading them to Confluence.

## Features

- **Fetch Jira Issue Details**: Retrieve and process detailed information about Jira issues.
- **Version Management**: Automatically increment version numbers in Jira issues.
- **Document Processing**: Convert `.docx` files to HTML format and process them, including extracting images and embedding them as base64 in HTML.
- **Confluence Integration**: Upload images and update or create Confluence pages with new HTML content.

## Prerequisites

- Python 3.8 or later
- Docker (optional, for containerized deployment)
- Jira and Confluence accounts with API tokens

#### Note
Make sure to install all Pandoc in system and set the path variable.

## Installation (Without Docker)

### 1. Clone the Repository

```bash
git clone https://github.com/axs7941onemindservices/JIraIntegrator.git
cd JIraIntegrator
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

Before running the application, set the following environment variables:

- **JIRA_API_TOKEN**: Your Jira API token.
- **EMAIL**: The email of the account used as the integrator.

You can set these variables in a `.env` file or directly in your environment.

## Running the Application

### 1. Start the FastAPI Server

Run the FastAPI server locally by running:

```bash
uvicorn main:app --reload
```

The server will be accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 2. Example API Endpoint

#### Upload to Confluence

To upload the latest `.docx` attachment from a Jira issue to Confluence, use the following endpoint:

**Endpoint**: `POST /Upload_to_confluence`

**Request Body**:

```json
{
    "issue_key": "DV-238"
}
```

This will:
1. Increment the version number.
2. Fetch issue details from Jira.
3. Download the latest `.docx` file attached to the Jira issue.
4. Convert the `.docx` to Markdown and then to HTML.
5. Extract images, save them, and embed them as base64 in the HTML.
6. Upload the content to a Confluence page, either creating a new page or updating an existing one based on the title extracted from the document.

## Running the Application with Docker

### Dockerfile Overview

The project includes a **Dockerfile** that allows you to run the application inside a container. The Dockerfile is designed to:

- Install dependencies such as **pandoc** (for document conversion) and **Python dependencies**.
- Set up the environment for running the FastAPI server inside Docker.

### 1. Build the Docker Image

In the root directory of the project, build the Docker image:

```bash
docker build -t jira-integrator .
```

### 2. Run the Docker Container

Run the Docker container with the FastAPI application:

```bash
docker run -p 8000:8000 jira-integrator
```

This will start the application on [http://localhost:8000](http://localhost:8000).

### Example Docker Command for Development

If you want to enable hot-reloading during development (similar to the FastAPI `--reload` flag), you can modify the `CMD` instruction in the Dockerfile or run the container with:

```bash
docker run -p 8000:8000 -v $(pwd):/main jira-integrator
```

This mounts your local directory inside the container, allowing you to see changes without rebuilding the Docker image.

## Development

### Code Structure

- **`main.py`**: Entry point for the FastAPI application.
- **`models/request_schemas.py`**: Pydantic models used for request validation.
- **`utils/increment_version.py`**: Contains the `increment_version` function for managing version numbers.
- **`processors/fetch_issue_details.py`**: Logic for fetching Jira issue details.
- **`processors/process_download_attachment.py`**: Handles downloading and converting `.docx` files to Markdown and HTML.
- **`processors/confluence_uploader.py`**: Manages uploading content to Confluence.

### Running Unit Tests

To run tests, make sure you have installed the necessary testing dependencies, then run:

```bash
pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### **Dockerfile Summary**:

The **Dockerfile** is designed to run the Jira Integrator project inside a container, with Pandoc and Python dependencies pre-installed:

```Dockerfile
# Use Python 3.10 base image
FROM python:3.10-slim

# Install pandoc and wget
RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download and install Pandoc manually
RUN wget https://github.com/jgm/pandoc/releases/download/3.1.8/pandoc-3.1.8-linux-amd64.tar.gz -O pandoc.tar.gz \
    && tar -xzf pandoc.tar.gz --strip-components 1 -C /usr/local/ \
    && rm pandoc.tar.gz

# Verify Pandoc installation
RUN pandoc --version

# Set the working directory
WORKDIR /main

# Copy the requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the FastAPI application code to the container
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to start FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### Steps to Use Dockerfile:
1. **Build** the image with:
   ```bash
   docker build -t jira-integrator .
   ```
2. **Run** the container:
   ```bash
   docker run -p 8000:8000 jira-integrator
   ```
