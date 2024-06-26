from PyPDF2 import PdfReader
def get_pdf_text(file):
    """
    Retrieves the text content from a PDF file.

    Parameters:
        file (str): The path to the PDF file.

    Returns:
        str: The concatenated text content extracted from the PDF file.
    """
    try:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except PermissionError as e:
        raise PermissionError(f"Permission denied: {e}")
    except ValueError as e:
        raise ValueError(f"Error reading PDF file: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")