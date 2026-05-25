import logging
import sys

log_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Set up logging to stdout
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(log_format)

# Set up logging to a file
file_handler = logging.FileHandler("../../logs/app.log")
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(log_format)