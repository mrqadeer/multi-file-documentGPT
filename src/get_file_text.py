import os
import streamlit as st
from src.pdf_reader import get_pdf_text
from src.docx_reader import get_docx_text
def get_file_text(uploaded_files):
    """
    Retrieves the text content from a list of uploaded files.

    Args:
        uploaded_files (List[streamlit.File]): A list of uploaded files.

    Returns:
        str: The concatenated text content extracted from the uploaded files.

    Raises:
        streamlit.errors.StopException: If the file extension is neither '.pdf' nor '.docx'.

    """
    text = ""
    for uploaded_file in uploaded_files:
        split_up = os.path.splitext(uploaded_file.name)
        file_extension = split_up[1]
        if file_extension == '.pdf':
            text += get_pdf_text(uploaded_file)
        elif file_extension == '.docx':
            text += get_docx_text(uploaded_file)
        else:
            st.stop()
    return text