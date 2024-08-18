import pypandoc


def docx_to_markdown(docx_file_path):
    # Convert the .docx file to markdown and save it
    markdown_content = pypandoc.convert_file(docx_file_path, 'md')
    return markdown_content
