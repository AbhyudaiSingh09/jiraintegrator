# from logger_config import logger as logger 

# def read_html_file(file_path):
#     """Reads and returns the content of an HTML file."""
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             html_content = file.read()
#         return html_content
#     except FileNotFoundError:
#         logger.error(f"File not found: {file_path}")
#         return None

import aiofiles
from logger_config import logger

async def read_html_file(file_path: str) -> str:
    """Reads and returns the content of an HTML file asynchronously."""
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
            html_content = await file.read()
        return html_content
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"An error occurred while reading {file_path}: {e}")
        return None