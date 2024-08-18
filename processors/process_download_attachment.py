
import requests
from logger_config import logger as logger
import os
from processors.docx_to_markdown_conversion import docx_to_markdown

# Define the paths for the input .docx file and output README.md file'
output_file_path = 'README.md'


def download_attachment(attachment_url,updated_request_body, filename):
    # Set the headers for the request, including the authorization token
    headers = {
        'Authorization': f'Basic {updated_request_body.api_token_v1}'
    }
    # Send a GET request to download the attachment
    response = requests.get(attachment_url, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        # Save the attachment to a file
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    else:
        # Log an error message if the download failed
        logger.error(f"Failed to download document: {response.status_code} - {response.text}")
        return ""


def process_attachments(updated_request_body,issue_details):
    # Check if the issue data contains attachments
    if 'fields' in issue_details and 'attachment' in issue_details['fields']:
        attachments = issue_details['fields']['attachment']
        # Loop through each attachment
        for attachment in attachments:
            # Look for .docx files
            if attachment['filename'].endswith('.docx'):
                attachment_url = attachment['content']
                # filename = 'document.docx'
                filename = attachment['filename']
                # Download the .docx file
                downloaded_file = download_attachment(attachment_url,updated_request_body,filename)

                if downloaded_file:
                    # Extract content from the downloaded .docx file
                    markdown_content= docx_to_markdown(downloaded_file)
                    # Clean up the downloaded file
                    os.remove(downloaded_file)
                    logger.info("Content has been extracted and returned!")
                    return markdown_content
        
        # Log an info message if no .docx attachments were found
        logger.warning("No .docx attachments found.")
    else:
        # Log an info message if the issue has no attachments
        logger.warning("No attachments field in issue data.")
    
    return None