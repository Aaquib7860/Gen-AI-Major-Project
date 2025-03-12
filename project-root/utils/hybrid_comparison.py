from models.hybrid_model import traditional_comparison, llm_comparison, process_diff

def hybrid_comparison(text1, text2):
    """
    Hybrid approach combining traditional and LLM-based comparison.
    """
    traditional_result = traditional_comparison(text1, text2)
    process_result1, process_result2  = process_diff(traditional_result)
    llm_result = llm_comparison(text1, text2)

    return {
        "process_diff": [process_result1, process_result2],
        "llm": llm_result
    }


