
import asyncio
import pypandoc
from logger_config import logger  # Assuming you have a logger configured
from processors import write_to_mardownfile  # Assuming this is your module

async def docx_to_markdown(docx_file_path: str) -> str:
    try:
        # Convert the .docx file to markdown asynchronously
        markdown_content = await asyncio.to_thread(pypandoc.convert_file, docx_file_path, 'md')
        
        # Write the markdown content to a file asynchronously
        markdownfilename = await write_to_mardownfile.write_content_to_markdownfile(markdown_content, docx_file_path)
        
        logger.info(f"Markdown file created: {markdownfilename}")
        return markdownfilename

    except Exception as e:
        logger.error(f"An error occurred during the docx to markdown conversion: {e}")
        return None