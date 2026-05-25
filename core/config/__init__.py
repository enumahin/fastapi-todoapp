import os
from dotenv import load_dotenv

from core.config import jwt_config

# Load environment variables
try:
    load_dotenv(override=False)
except Exception as e:
    print(e)

ENV = os.getenv('ENV')
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB


# Email config
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = os.getenv('MAIL_PORT')
MAIL_USE_SSL = os.getenv('MAIL_USE_SSL') == 'True'
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
