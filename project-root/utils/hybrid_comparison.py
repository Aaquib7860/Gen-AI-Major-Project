from models.hybrid_model import traditional_comparison
from models.hybrid_model import llm_comparison

def hybrid_comparison(text1, text2, api_key):
    """
    Hybrid approach combining traditional and LLM-based comparison.
    """
    traditional_result = traditional_comparison(text1, text2)
    llm_result = llm_comparison(text1, text2, api_key)

    return {
        "traditional": traditional_result,
        "llm": llm_result
    }
