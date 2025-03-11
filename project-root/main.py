import os
import streamlit as st
from dotenv import load_dotenv
from utils.hybrid_model import hybrid_comparison
from utils.highlight import merge_results

# Load API key once
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ Error: GROQ_API_KEY not found! Check your .env file.")

# Input texts
text1 = st.text_area("Enter first document:")
text2 = st.text_area("Enter second document:")

if st.button("Compare"):
    results = hybrid_comparison(text1, text2, api_key)
    merged_output = merge_results(results["traditional"], results["llm"])

    st.write("\nFinal Merged Comparison:\n", merged_output)
