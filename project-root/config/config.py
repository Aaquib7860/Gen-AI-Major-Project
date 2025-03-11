import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API Key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ Error: GROQ_API_KEY not found! Check your .env file.")

# Groq API Settings
GROQ_MODEL = "mixtral-8x7b-32768"  # Change model if needed
MAX_TOKENS = 500  # Limit token usage
TEMPERATURE = 0.2  # Adjust creativity level
