import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
AUTOACT_API_KEY = os.getenv('AUTOACT_API_KEY')
AUTOACT_API_BASE_URL = os.getenv('AUTOACT_API_BASE_URL', 'http://localhost:3000/api')

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

# File to store the AutoAct API key
AUTOACT_API_KEY_FILE = 'autoact_api_key.txt'
