import requests
from logger_config import logger as logger
from processors import docx_to_markdown_conversion,get_images,image_converter,markdown_to_html,create_confluencepage
from utils import read_htmlfile,garbage_collector
import aiofiles
import os




async def download_attachment(attachment_url,updated_request_body, filename,yaml_config):

    temp_folder = yaml_config.Folder.temp_folder
    
    # Ensure the folder exists
    os.makedirs(temp_folder, exist_ok=True)
    
    # Construct the full path to the file in the temporary folder
    file_path = os.path.join(temp_folder, filename)

    # Set the headers for the request, including the authorization token
    headers = {
        'Authorization': f'Basic {updated_request_body.api_token_v1}'
    }
    # Send a GET request to download the attachment
    response = requests.get(attachment_url, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(response.content)
        logger.info(f"content has been downloaded from Jira for issue {updated_request_body.issue_Key} and stored in {file_path}")
        return file_path
    else:
        # Log an error message if the download failed
        logger.error(f"Failed to download document: {response.status_code} - {response.text}")
        return ""




async def process_attachments(updated_request_body,issue_details,yaml_config):
    # Check if the issue data contains attachments
    if 'fields' in issue_details and 'attachment' in issue_details['fields']:
        attachments = issue_details['fields']['attachment']
        # Loop through each attachment
        for attachment in attachments:
            # Look for .docx files
            if attachment['filename'].endswith('.docx'):
                attachment_url = attachment['content']
                # filename = 'document.docx'
                basefilepath = attachment['filename']
                # Download the .docx file
                downloaded_file_path = await download_attachment(attachment_url,updated_request_body,basefilepath,yaml_config)

                if downloaded_file_path:
                    # Extract content from the downloaded .docx file
                    # Images
                    basefolder_path=  await get_images.extract_images_from_docx(downloaded_file_path,yaml_config)
                    # text
                    markdownfilename=  await docx_to_markdown_conversion.docx_to_markdown(downloaded_file_path)
                    # confluence_pageid = await create_confluencepage.create_confluence_page(yaml_config,updated_request_body)
                    # print(confluence_pageid)
                    html_filename_path = await markdown_to_html.write_content_to_htmlfile(markdownfilename)
                   
                    input_html_file_path=output_html_file_path= html_filename_path
                    await image_converter.replace_images_with_base64_in_html(input_html_file_path,basefolder_path,output_html_file_path)
                    html_content = await read_htmlfile.read_html_file(html_filename_path)

                    logger.info(f"Content and Images have been extracted and written to {html_filename_path},{basefolder_path}!")
                    basefilepath=basefilepath.rstrip('.docx')
                    await garbage_collector.remove_files_and_folder(basefilepath,yaml_config)
                    return html_content
        
        # Log an info message if no .docx attachments were found
        logger.warning("No .docx attachments found.")
    else:
        # Log an info message if the issue has no attachments
        logger.warning("No attachments field in issue data.")
    
    return None
