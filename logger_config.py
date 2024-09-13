import logging

# Create a custom logger
logger = logging.getLogger(__name__)

# Set the default log level
logger.setLevel(logging.DEBUG)  
    
# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("logs/app.log")

# Set log levels for handlers
console_handler.setLevel(
    logging.INFO
)  # Console will show INFO and above (INFO, WARNING, ERROR, CRITICAL)
file_handler.setLevel(
    logging.INFO
)  # File will log WARNING and above (WARNING,ERROR, CRITICAL)

# Create formatters and add them to handlers
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
