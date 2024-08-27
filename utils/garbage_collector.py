import os
import shutil
from logger_config import logger as logger

def remove_files_and_folder(base_filename):
    """Removes .md, .html, .docx files and a folder based on the base filename."""
    try:
        # Define the file extensions to be removed
        extensions = ['.md', '.html', '.docx']
        
        # Remove the files
        for ext in extensions:
            file_path = base_filename + ext
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Removed file: {file_path}")
            else:
                logger.info(f"File not found: {file_path}")

        # Remove the folder
        folder_path = base_filename
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
            logger.info(f"Removed folder: {folder_path}")

        # Log success
        logger.info("Garbage Collector ran successfully.")

        return " "

    except Exception as e:
        # Log any errors that occur
        logger.error(f"An error occurred: {e}")
        return ""

