import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")  # Default to gpt-4o-mini if not set
AUTONOMEEE_API_URL = "https://api.autonomeee.com"
API_KEY_FILE = "agent_api_key.txt"