import re

def highlight_differences(traditional_diff, llm_diff=None):
    highlighted_text1 = ""
    highlighted_text2 = ""
    change_summary = ""

    for diff in traditional_diff:
        action = diff[:2]
        text = diff[2:].strip()

        if action == "+ ":
            highlighted_text1 += f'<span style="color:green;">{text} </span>'  # Green for additions
            highlighted_text2 += f'{text} '
            change_summary += f'Added: {text} <br>'
        elif action == "- ":
            highlighted_text1 += f'{text} '
            highlighted_text2 += f'<span style="color:red;">{text} </span>'  # Red for deletions
            change_summary += f'Removed: {text} <br>'
        elif action == "? ":
            text = re.sub(r'(\S+)', r'<span style="background-color:yellow; color:black;">\1</span>', text)
            highlighted_text1 += f'{text} '
            highlighted_text2 += f'{text} '
            change_summary += f'Modified: {text} <br>'
        else:
            highlighted_text1 += f'{text} '
            highlighted_text2 += f'{text} '

    if llm_diff:
        change_summary += "<br><b>LLM Insights:</b><br>" + llm_diff

    return highlighted_text1, highlighted_text2
