import os
import shutil
import asyncio
from logger_config import logger

async def remove_files_and_folder(base_filename: str,yaml_config: dict) -> str:
    """Asynchronously removes .md, .html, .docx files and a folder based on the base filename."""
    try:
        temp_folder_path = yaml_config['Folder']['temp_folder']

        # Define the file extensions to be removed
        extensions = ['.md', '.html', '.docx']
        
        # Remove the files asynchronously
        for ext in extensions:
            file_path = temp_folder_path + base_filename + ext
            if os.path.exists(file_path):
                await asyncio.to_thread(os.remove, file_path)
                logger.info(f"Removed file: {file_path}")
            else:
                logger.info(f"File not found: {file_path}")

        # Remove the folder asynchronously
        folder_path = temp_folder_path + base_filename
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            await asyncio.to_thread(shutil.rmtree, folder_path)
            logger.info(f"Removed folder: {folder_path}")

        # Log success
        logger.info("Garbage Collector ran successfully.")

        return " "

    except Exception as e:
        # Log any errors that occur
        logger.error(f"An error occurred: {e}")
        return ""