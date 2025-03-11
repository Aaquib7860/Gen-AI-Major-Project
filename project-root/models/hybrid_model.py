import difflib
from groq import Groq
from utils.config import GROQ_API_KEY, GROQ_MODEL, MAX_TOKENS, TEMPERATURE

def traditional_comparison(text1, text2):
    """
    Perform traditional text comparison using difflib.
    """
    diff = list(difflib.ndiff(text1.split(), text2.split()))
    return diff

def llm_comparison(text1, text2):
    """
    Perform LLM-based document comparison using Groq API.
    """
    client = Groq(api_key=GROQ_API_KEY)  # Use API key from config

    prompt = f"Compare these two documents and highlight the differences:\n\nDocument 1:\n{text1}\n\nDocument 2:\n{text2}"

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are an AI assistant that compares documents and highlights differences."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE
    )

    return response.choices[0].message.content.strip()
