import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AUTOACT_API_KEY = os.getenv("AUTOACT_API_KEY")
AUTOACT_API_BASE_URL = os.getenv("AUTOACT_API_BASE_URL")
