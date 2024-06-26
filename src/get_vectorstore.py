from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.vectorstores import FAISS
def get_vectorstore(text_chunks):
    """
    Generate a vector store for the given text chunks using HuggingFaceEmbeddings.

    Args:
        text_chunks (List[str]): A list of text chunks to be embedded.

    Returns:
        knowledge_base (FAISS): The vector store created from the text chunks using HuggingFaceEmbeddings.
    """
    embedding = HuggingFaceEmbeddings(
        model_name=st.session_state.embedding_model)

    # embedding = OpenAIEmbeddings(openai_api_key=st.session_state.api_key)
    knowledge_base = FAISS.from_texts(text_chunks, embedding)
    return knowledge_base