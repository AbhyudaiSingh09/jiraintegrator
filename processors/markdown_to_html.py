import asyncio
import aiofiles
import pypandoc
from logger_config import logger


async def write_content_to_htmlfile(filename: str) -> str:
    try:
        # Convert markdown to HTML asynchronously using a thread
        html_content = await asyncio.to_thread(pypandoc.convert_file, filename, "html")

        # Create file name for HTML
        html_filename_path = filename.rstrip(".md") + ".html"

        # Write the HTML content to a file asynchronously
        async with aiofiles.open(html_filename_path, "w") as f:
            await f.write(html_content)

        logger.info(f"HTML file created: {html_filename_path}")
        return html_filename_path

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None
