import aiofiles
from logger_config import logger


async def write_content_to_markdownfile(markdown_content: str, filename: str) -> str:
    # Create file name
    filename = filename.rstrip(".docx") + ".md"
    try:
        # Write to markdown file asynchronously
        async with aiofiles.open(filename, "w") as f:
            await f.write(markdown_content)
        logger.info(f"Successfully wrote to {filename}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e
    return filename
