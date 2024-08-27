import pypandoc
from processors import write_to_mardownfile


def docx_to_markdown(docx_file_path) -> str:
    # Convert the .docx file to markdown and save it
    markdown_content = pypandoc.convert_file(docx_file_path, 'md')
    markdownfilename = write_to_mardownfile.write_content_to_markdownfile(markdown_content,docx_file_path)
    return markdownfilename
