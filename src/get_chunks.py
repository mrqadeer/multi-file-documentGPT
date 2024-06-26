from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
def get_file_chunks(file):
    """
    Function to get file chunks using RecursiveCharacterTextSplitter.

    Parameters:
    file (str): The file to split into chunks.

    Returns:
    list: List of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        separator=['\n','\n\n',',','.'],
        chunk_size=900,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(file)
    # st.write(chunks)
    return chunks