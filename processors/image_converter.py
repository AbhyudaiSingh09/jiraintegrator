import os
import base64
import re
import aiofiles
from logger_config import logger  # Assuming you have a logger configured


async def encode_image_to_base64(image_path: str) -> str:
    """Encodes an image to a Base64 string asynchronously."""
    try:
        async with aiofiles.open(image_path, "rb") as image_file:
            image_data = await image_file.read()
            return base64.b64encode(image_data).decode("utf-8")
    except Exception as e:
        logger.error(f"Failed to encode image {image_path} to Base64: {e}")
        return None


async def replace_images_with_base64_in_html(
    html_file_path: str, images_folder: str, output_html_file_path: str
):
    """Replaces image paths in HTML with Base64-encoded images asynchronously."""
    if not html_file_path or not images_folder or not output_html_file_path:
        logger.error(
            "Invalid input parameters: NoneType found in html_file_path, images_folder, or output_html_file_path."
        )
        return

    # Read the HTML content from the file
    try:
        async with aiofiles.open(html_file_path, "r", encoding="utf-8") as file:
            html_content = await file.read()
    except Exception as e:
        logger.error(f"Failed to read HTML file {html_file_path}: {e}")
        return

    # Find all image tags with src attributes
    image_tags = re.findall(r'<img\s+[^>]*src="([^"]+)"[^>]*>', html_content)

    for img_tag in image_tags:
        # Extract the image filename from the src attribute
        image_filename = os.path.basename(img_tag)

        if not image_filename:
            logger.warning(
                f"Skipping image with empty filename found in {html_file_path}"
            )
            continue

        image_path = os.path.join(images_folder, image_filename)

        if os.path.exists(image_path):
            # Encode the image to Base64 asynchronously
            base64_str = await encode_image_to_base64(image_path)
            if base64_str:
                base64_image = f"data:image/png;base64,{base64_str}"

                # Replace the image path with the Base64-encoded string in the HTML content
                html_content = html_content.replace(
                    f'src="{img_tag}"', f'\nsrc="{base64_image}"'
                )
            else:
                logger.error(f"Failed to encode image {image_filename} at {image_path}")
        else:
            logger.warning(f"Image file {image_path} not found. Skipping this image.")

    # Write the modified HTML content to a new file asynchronously
    try:
        async with aiofiles.open(
            output_html_file_path, "w", encoding="utf-8"
        ) as output_file:
            await output_file.write(html_content)
        logger.info(f"Updated HTML content saved to {output_html_file_path}")
    except Exception as e:
        logger.error(
            f"Failed to write updated HTML content to {output_html_file_path}: {e}"
        )
