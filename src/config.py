"""
Configuration settings for the Redis Excel Integration project.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Redis configuration
# Default to Redis Cloud instance, fallback to localhost
REDIS_HOST = os.getenv('REDIS_HOST', 'redis-13774.c322.us-east-1-2.ec2.redns.redis-cloud.com')
REDIS_PORT = int(os.getenv('REDIS_PORT', 13774))
REDIS_DB = int(os.getenv('REDIS_DB', 0))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', 'vTL3XqF3Nwpnnq6Ti2pY7AukjTX0DzDm')
REDIS_USERNAME = os.getenv('REDIS_USERNAME', 'default')

# File paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
SAMPLE_EXCEL_FILE = os.path.join(DATA_DIR, 'sample_data.xlsx')

# Excel configuration
DEFAULT_SHEET_NAME = 'Sheet1'
MAX_ROWS = 10000  # Maximum rows to process
