import os
from dotenv import load_dotenv

# Load environment variables from .env file

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Error: GROQ_API_KEY not found! Check your .env file.")

# Groq API Settings
GROQ_MODEL = "llama-3.3-70b-versatile"  # Change model if needed
MAX_TOKENS = None  # Limit token usage
TEMPERATURE = 0.2  # Adjust creativity level
