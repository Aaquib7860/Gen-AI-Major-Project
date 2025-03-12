import difflib
from groq import Groq
from config.config import GROQ_API_KEY, GROQ_MODEL, MAX_TOKENS, TEMPERATURE

def traditional_comparison(text1, text2):
    """
    Perform traditional text comparison using difflib.
    """
    diff = list(difflib.ndiff(text1.split(), text2.split()))
    return diff


def process_diff(diff):
    """Process diff output and generate highlighted HTML for both texts"""
    text1_html = []
    text2_html = []
    i = 0
    
    for item in diff:
        if item.startswith('- '):  # Removed from text1
            text1_html.append(f'<span style="background-color: #ffcccc">{item[2:]}</span>')
        elif item.startswith('+ '):  # Added to text2
            text2_html.append(f'<span style="background-color: #ccffcc">{item[2:]}</span>')
        elif item.startswith('  '):  # Unchanged
            text1_html.append(f'<span>{item[2:]}</span>')
            text2_html.append(f'<span>{item[2:]}</span>')
        i += 1
    
    return ' '.join(text1_html), ' '.join(text2_html)

def llm_comparison(text1, text2):
    """
    Perform LLM-based document comparison using Groq API.
    """

    max_chars = 12000

    text1 = text1[:max_chars]  
    text2 = text2[:max_chars]

    client = Groq(api_key=GROQ_API_KEY)

    prompt = f"Compare these two documents and highlight the differences:\n\nDocument 1:\n{text1}\n\nDocument 2:\n{text2}"

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are an AI assistant that compares documents and summarize the sementic differences."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE
    )

    return response.choices[0].message.content.strip()



