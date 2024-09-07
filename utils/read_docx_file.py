from docx import Document
from logger_config import logger
import asyncio

async def get_page_title(docx_file_path: str) -> str:
    print(f"docx_file_path:{docx_file_path}")
    """Extracts and returns the text content of the first heading in a DOCX file asynchronously."""
    try:
        # Ensure the file exists and load the DOCX file asynchronously
        doc = await asyncio.to_thread(Document, docx_file_path)

        # Iterate over the paragraphs in the DOCX file to find the first heading
        for para in doc.paragraphs:
            if para.style.name.startswith('Heading'):
                logger.info(f"Page Title extracted: {para.text.strip()}")
                print(f"para.text.strip():{para.text.strip()}")
                return para.text.strip()

        # If no headings are found, log a warning and return None
        logger.warning(f"No headings found in {docx_file_path}")
        return None

    except FileNotFoundError:
        logger.error(f"File not found: {docx_file_path}")
        return None
    except Exception as e:
        logger.error(f"An error occurred while reading {docx_file_path}: {e}")
        return None