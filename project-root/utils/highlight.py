import re

def highlight_differences(traditional_diff, llm_diff=None):
    """
    Highlights differences using HTML formatting for visualization in Streamlit.
    
    Args:
        traditional_diff (list): List of differences from difflib.
        llm_diff (str, optional): Additional LLM insights.
    
    Returns:
        str: HTML formatted text for Streamlit display.
    """
    highlighted_text = ""

    for diff in traditional_diff:
        action = diff[:2]
        text = diff[2:].strip()

        if action == "+ ":
            highlighted_text += f'<span style="color:green;">{text} </span>'  # Green for additions
        elif action == "- ":
            highlighted_text += f'<span style="color:red;">{text} </span>'  # Red for deletions
        elif action == "? ":
            # Highlight modified words in yellow
            text = re.sub(r'(\S+)', r'<span style="background-color:yellow; color:black;">\1</span>', text)
            highlighted_text += f'{text} '
        else:
            highlighted_text += f'{text} '  # Normal text

    # If LLM insights are available, append them
    if llm_diff:
        highlighted_text += "<br><br><b>LLM Insights:</b><br>" + llm_diff

    return highlighted_text
