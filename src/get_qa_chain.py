import openai
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def get_conversation_chain(vectprstore):
    """
    Generate a conversation chain using the given vector store.

    Args:
        vectprstore (VectorStore): The vector store to use for retrieval.

    Returns:
        ConversationalRetrievalChain: The generated conversation chain.

    Raises:
        None

    Notes:
        - This function creates a ChatOpenAI model with the OpenAI API key stored in the session state.
        - The temperature for the model is set to the value stored in the session state.
        - A ConversationBufferMemory is created with the memory key 'chat_history' and set to return messages.
        - The conversation chain is created using the ChatOpenAI model, the ConversationBufferMemory, and the vector store retriever.
        - The generated conversation chain is returned.
    """
    try:
        llm = ChatOpenAI(openai_api_key=st.session_state.api_key,
                     #  model_name='gpt-3.5-turbo',
                     temperature=st.session_state.temperature,
                     )
        memory = ConversationBufferMemory(memory_key='chat_history',
                                        return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(

            llm=llm,
            memory=memory,
            retriever=vectprstore.as_retriever()
        )
        return conversation_chain
    except openai.error.InvalidRequestError as e:
        st.error(f"Invalid request: {e}")
    except openai.error.AuthenticationError as e:
        st.error(f"Authentication error: {e}")
    except openai.error.PermissionError as e:
        st.error(f"Permission error: {e}")
    except openai.error.RateLimitError as e:
        st.error(f"Rate limit exceeded: {e}")
    except openai.error.Timeout as e:
        st.error(f"Request timed out: {e}")
    except openai.error.APIConnectionError as e:
        st.error(f"Network connection error: {e}")
    except openai.error.ServiceUnavailableError as e:
        st.error(f"Service unavailable: {e}")
    except openai.error.APIError as e:
        st.error(f"API error: {e}")
    except openai.error.SignatureVerificationError as e:
        st.error(f"Signature verification error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")