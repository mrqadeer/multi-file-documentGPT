from docx import Document

def get_docx_text(file):
    """
    Retrieves the text content from a DOCX file.

    Parameters:
    file (str): The path to the DOCX file.

    Returns:
    str: The concatenated text content extracted from the DOCX file.
    """
    documemt = Document(file)
    AllText = []
    for document_paragraph in documemt.paragraphs:
        AllText.append(document_paragraph.text)
    text = " ".join(AllText)
    return text
