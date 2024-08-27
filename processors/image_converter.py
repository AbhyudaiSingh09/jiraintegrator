import os
import base64
import re

def encode_image_to_base64(image_path):
    """Encodes an image to a Base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def replace_images_with_base64_in_html(html_file_path, images_folder, output_html_file_path):
    """Replaces image paths in HTML with Base64-encoded images."""

    # Read the HTML content from the file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Find all image tags with src attributes
    image_tags = re.findall(r'<img\s+[^>]*src="([^"]+)"[^>]*>', html_content)

    for img_tag in image_tags:
        # Extract the image filename from the src attribute
        image_filename = os.path.basename(img_tag)
        image_path = os.path.join(images_folder, image_filename)

        if os.path.exists(image_path):
            # Encode the image to Base64
            base64_str = encode_image_to_base64(image_path)
            base64_image = f"data:image/png;base64,{base64_str}"

            # Replace the image path with the Base64-encoded string in the HTML content
            html_content = html_content.replace(f'src="{img_tag}"', f'src="{base64_image}"')

    # Write the modified HTML content to a new file
    with open(output_html_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(html_content)

    print(f"Updated HTML content saved to {output_html_file_path}")
