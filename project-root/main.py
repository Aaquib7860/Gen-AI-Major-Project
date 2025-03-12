import streamlit as st
import difflib
import base64
from utils.hybrid_comparison import hybrid_comparison
from utils.file_handler import FileHandler, loading_doc


st.title("Text Comparison Tool")

# File Upload Section
text1 = st.sidebar.file_uploader("Upload your first file here.", type=["txt", "docx", "pdf", "ppt", "pptx"])
text2 = st.sidebar.file_uploader("Upload your second file here.", type=["txt", "docx", "pdf", "ppt", "pptx"])

text_data = loading_doc(text1, text2)

# Create side-by-side layout for documents
col1, col2 = st.columns(2)

doc1, doc2 = "", ""

if text_data is not None:
    with col1:
        st.subheader("📂 Document 1")
        doc1 = st.text_area("Paste or upload Document 1:", text_data[0], height=400)

    with col2:
        st.subheader("📂 Document 2")
        doc2 = st.text_area("Paste or upload Document 2:", text_data[1], height=400)

if st.button("Compare Texts"):
    if text1 and text2:
        
        differences = hybrid_comparison(text_data[0], text_data[1])

        
        # Display results in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("File 1 (Original) - Differences")
            st.markdown(
                f'<div style="padding: 10px; border: 1px solid #ddd; min-height: 400px; max-height:400px; overflow-y: auto; white-space: pre-wrap;">{differences['process_diff'][0]}</div>',
                unsafe_allow_html=True
            )
            st.markdown("*Red: Words removed in File 2*")
        
        with col2:
            st.subheader("File 2 (Modified) - Differences")
            st.markdown(
                f'<div style="padding: 10px; border: 1px solid #ddd; min-height: 400px; max-height:400px; overflow-y: auto; white-space: pre-wrap;">{differences['process_diff'][1]}</div>',
                unsafe_allow_html=True
            )
            st.markdown("*Green: Words added in File 2*")

        st.subheader("Summary")
        st.markdown(differences['llm'], unsafe_allow_html=True)
        # st.sidebar.markdown(f'<a href="data:file/txt;base64,{base64.b64encode(differences["merged_output"].encode()).decode()}" download="comparison_results.txt">📥 Download Comparison Results</a>', unsafe_allow_html=True)
    else:
        st.error("Please enter text in both fields")
