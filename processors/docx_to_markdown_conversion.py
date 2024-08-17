from docx import Document
import os


output_file_path = 'README.md'

def docx_to_markdown(docx_file_path):
    # Load the .docx file
    doc = Document(docx_file_path)
    
    # Initialize an empty list to hold the lines of the markdown content
    markdown_content = []
    
    # Iterate over each paragraph in the .docx file
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            markdown_content.append(text)
    
    # Join all the lines into a single string with newline characters
    markdown_text = "\n\n".join(markdown_content)
    
    # Write the markdown text to the output file
    with open(output_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(markdown_text)

    print(f"Markdown content has been written to {output_file_path}")



