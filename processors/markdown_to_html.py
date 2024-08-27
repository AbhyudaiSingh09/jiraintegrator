import pypandoc
from logger_config import logger as logger


def write_content_to_htmlfile(filename):
    try:
        html_content= pypandoc.convert_file(filename, 'html')
    
        #Create file name for html
        html_filename = filename.rstrip('.md') + ".html"
        
        #write to html file
        with open(html_filename, 'w') as f:
            f.write(html_content)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    
    return html_filename