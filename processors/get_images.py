# import os
# from docx import Document

# def extract_images_from_docx(docx_path):
#     # Load the document
#     doc = Document(docx_path)

#     # Extract the base filename (without extension) to use as the folder name
#     base_filename = os.path.splitext(os.path.basename(docx_path))[0]
#     output_folder = base_filename

#     # Create the output folder if it doesn't exist
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     # Iterate over all the relationships in the document
#     image_count = 0
#     for rel in doc.part.rels.values():
#         if "image" in rel.target_ref:
#             image_count += 1
#             # Extract the image name from the relationship target reference
#             image_name = f"image{image_count}.png"
#             image_path = os.path.join(output_folder, image_name)
            
#             # Save the image to the output folder
#             with open(image_path, "wb") as img_file:
#                 img_file.write(rel.target_part.blob)
            
#             print(f"Saved {image_name} to {image_path}")

#     print(f"Extracted {image_count} images to folder: {output_folder}")

#     return output_folder

import os
import aiofiles
import asyncio 
from docx import Document
from logger_config import logger  # Assuming you have a logger configured

async def extract_images_from_docx(docx_path: str) -> str:
    try:
        # Load the document
        doc = await asyncio.to_thread(Document, docx_path)

        # Extract the base filename (without extension) to use as the folder name
        base_filename = os.path.splitext(os.path.basename(docx_path))[0]
        output_folder = base_filename

        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Iterate over all the relationships in the document
        image_count = 0
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                image_count += 1
                # Extract the image name from the relationship target reference
                image_name = f"image{image_count}.png"
                image_path = os.path.join(output_folder, image_name)
                
                # Save the image to the output folder asynchronously
                async with aiofiles.open(image_path, "wb") as img_file:
                    await img_file.write(rel.target_part.blob)
                
                logger.info(f"Saved {image_name} to {image_path}")

        logger.info(f"Extracted {image_count} images to folder: {output_folder}")

        return output_folder

    except Exception as e:
        logger.error(f"An error occurred while extracting images: {e}")
        return None