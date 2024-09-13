import requests
from logger_config import logger as logger
from processors import (
    docx_to_markdown_conversion,
    get_images,
    image_converter,
    markdown_to_html,
)
from utils import read_docx_file, read_html_file, garbage_collector
import aiofiles
import os


async def download_attachment(
    attachment_url, request_body, filename, confluence_config
):
    working_directory = confluence_config.working_directory

    # Ensure the folder exists
    os.makedirs(working_directory, exist_ok=True)

    # Construct the full path to the file in the temporary folder
    file_path = os.path.join(working_directory, filename)

    # Set the headers for the request, including the authorization token
    headers = {"Authorization": f"Basic {confluence_config.api_token_v1}"}
    # Send a GET request to download the attachment
    response = requests.get(attachment_url, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(response.content)
        logger.info(
            f"Attachment file has been downloaded from Jira for issue {request_body.issue_key} and stored in {file_path}"
        )
        return file_path
    else:
        # Log an error message if the download failed
        logger.error(
            f"Failed to download document: {response.status_code} - {response.text}"
        )
        return ""


async def process_attachments(request_body, issue_details, confluence_config):
    # Check if the issue data contains attachments
    if "fields" in issue_details and "attachment" in issue_details["fields"]:
        attachments = issue_details["fields"]["attachment"]
        # Loop through each attachment
        for attachment in attachments:
            # Look for .docx files
            if attachment["filename"].endswith(".docx"):
                attachment_url = attachment["content"]
                # filename = 'document.docx'
                basefilepath = attachment["filename"]
                # Download the .docx file
                downloaded_file_path = await download_attachment(
                    attachment_url, request_body, basefilepath, confluence_config
                )

                if downloaded_file_path:
                    page_title = await read_docx_file.get_page_title(
                        downloaded_file_path
                    )
                    logger.info(f"page_title has been extracted :{page_title}")
                    # Extract content from the downloaded .docx file
                    # Images
                    basefolder_path = await get_images.extract_images_from_docx(
                        downloaded_file_path, confluence_config
                    )
                    # text
                    markdownfilename = (
                        await docx_to_markdown_conversion.docx_to_markdown(
                            downloaded_file_path
                        )
                    )

                    # page_data =  create_confluencepage.create_confluence_page(confluence_config,request_body,page_title)

                    html_filename_path = (
                        await markdown_to_html.write_content_to_htmlfile(
                            markdownfilename
                        )
                    )

                    input_html_file_path = output_html_file_path = html_filename_path
                    await image_converter.replace_images_with_base64_in_html(
                        input_html_file_path, basefolder_path, output_html_file_path
                    )
                    html_content = await read_html_file.read_html_file(
                        html_filename_path
                    )

                    logger.info(
                        f"Content and Images have been extracted and written to {html_filename_path} in {basefolder_path}!"
                    )
                    basefilepath = basefilepath.rstrip(".docx")
                    await garbage_collector.remove_files_and_folder(
                        basefilepath, confluence_config
                    )

                    return html_content, page_title

        # Log an info message if no .docx attachments were found
        logger.warning("No .docx attachments found.")
    else:
        # Log an info message if the issue has no attachments
        logger.warning("No attachments field in issue data.")

    return None
