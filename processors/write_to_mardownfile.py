from logger_config import logger as logger



def write_content_to_markdownfile(markdown_content,filename):
    #Create file name 
    filename = filename.rstrip('.docx') + ".md"
    try:
        #wrirte to markdown file 
        with open(filename, 'w') as f:
            f.write(markdown_content)
    except Exception as e:
        print(f"An error occurred: {e}")
    return filename