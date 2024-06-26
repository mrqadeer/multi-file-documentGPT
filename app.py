import os
import tempfile
import streamlit as st
import time as t
# Custom modules
from templates.htmlTemplates import css, bot_template, user_template
from src.get_file_text import get_file_text
from src.get_chunks import get_file_chunks
from src.get_vectorstore import get_vectorstore
from src.get_qa_chain import get_conversation_chain
def initialization():
    """
    Initializes the page configuration, sets the page title and icon, and displays a title for the Document Chatbot.
    It also initializes a global variable 'data' with a list of names.
    It iterates over the names in the 'data' list and displays each name as a subheader.

    Parameters:
    None

    Returns:
    None
    """
    st.set_page_config(page_title='Document Master',
                       page_icon=':books:', initial_sidebar_state='collapsed')
    st.title('Document Chatbot by Qadeer')
    global data
    data = ['Sir Irfan Malik', 'Hope To Skill',
            'Artificial Intelligence Course']
    for name in data:
        st.subheader(name, divider='rainbow')


def main():
    """
    Initializes the main function and sets up the necessary global variables and session state. It also handles user input and processes the uploaded files.

    Parameters:
    None

    Returns:
    None
    """
    global process
    process = None
    st.write(css, unsafe_allow_html=True)
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''
    if 'temperature' not in st.session_state:
        st.session_state.temperature = ""
    if 'Processing' not in st.session_state:
        st.session_state.Processing = False
    if 'embedding_model' not in st.session_state:
        st.session_state.embedding_model = ""
    if 'conversation' not in st.session_state:
        st.session_state.conversation = None
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = None
    uploaded_files = None
    with st.sidebar:
        about = st.toggle("What and How this Chatbot Works?", key='info')
        if about:
            st.info(f"""Chatbot is exclusively to talk to Documents files. This Chatbot
                supports pdf files and MS Word files only. This chatbot is capable 
                to answer the question of multiple files at a time.Special thanks to {data[0]}""")
            st.info("""This Chatbot requires your name, your Openai API Key,Temperature for your
                    model,Embedding model for your files.Finally upload your file and you are good to go.""")
        st.sidebar.title('Requirments')
        username = st.text_input(
            'Full Name', placeholder='Enter your name').title()
        if username is not None and (username.isalpha() or username.__contains__(' ')):
            st.session_state.username = username
            st.success(f"Welcome {st.session_state.username}")
            my_api_key = st.text_input(
                'Enter your API Key', placeholder='Enter your API key', type='password')
            if my_api_key and my_api_key.startswith('sk-'):
                st.session_state.api_key = my_api_key
                st.success(f'Thanks {username} for providing your API Key')
                temp = st.slider('Temperature of LLM', 0.0,
                                 1.0, 0.5, key='temp_slider')
                st.write(f'Temperature {temp}')
                yes = st.toggle('Set Temperature', key='tem')

                if st.session_state.temperature is not None and yes:
                    st.session_state.temperature = temp
                    st.info(
                        f"Your LLM's temperature is set as {st.session_state.temperature}")
                    EmbeddingModel = st.radio('Choose your Embedding Model',
                                              ['all-MiniLM-L6-v2', 'bert-base-uncased',
                                               'bert-large-uncased', 'roberta-base',
                                               ],
                                              captions=['Pre Downloaded', 'On Demand Download',
                                                        'On Demanad Downlaod', 'On Demand Download'],
                                              index=0)
                    if EmbeddingModel == 'all-MiniLM-L6-v2':
                        st.session_state.embedding_model = EmbeddingModel
                        yes = st.toggle(
                            f"{st.session_state.username} are you sure to select   \"{st.session_state.embedding_model}\"? ", key='emb')
                    elif EmbeddingModel == 'bert-base-uncased':
                        st.session_state.embedding_model = EmbeddingModel
                        yes = st.toggle(
                            f"{st.session_state.username} are you sure to select  \"{st.session_state.embedding_model}\"? ", key='emb')
                    elif EmbeddingModel == 'bert-large-uncased':
                        st.session_state.embedding_model = EmbeddingModel
                        yes = st.toggle(
                            f"{st.session_state.username} are you sure to select  \"{st.session_state.embedding_model}\"? ", key='emb')
                    elif EmbeddingModel == 'roberta-base':
                        st.session_state.embedding_model = EmbeddingModel
                        yes = st.toggle(
                            f"{st.session_state.username} are you sure to select   \"{st.session_state.embedding_model}\"? ", key='emb')
                    else:
                        return -1
                    if st.session_state.embedding_model is not None and yes:
                        st.success(
                            f"{st.session_state.username} you can now upload your file(s)")
                        uploaded_files = st.file_uploader(
                            f"{st.session_state.username} upload your files", type=['pdf', 'docx'],
                            accept_multiple_files=True)
                        if uploaded_files:
                            yes = st.toggle(f"Dear {st.session_state.username} are you done with Prerequisites?",
                                            key='done')
                            if yes:
                                st.success(
                                    f"Dear {st.session_state.username} press Submit to chat.")
                                process = st.button('Submit')
                            else:
                                st.stop()
                        else:
                            st.error(
                                f'{st.session_state.username} upload file to continue')
                            st.stop()
    if process:
        with st.status("Processing in progress...", expanded=True) as status:
            st.write("Uploading Files")
            t.sleep(2)
            files_text = get_file_text(uploaded_files)
            st.info(f'{st.session_state.username} your file(s) loaded')
            st.write("Making Chunks")
            t.sleep(2)
            text_chunks = get_file_chunks(files_text)
            st.info(f"{st.session_state.username} your file's chunks are created")
            st.write("Vectorizing Chunks")
            t.sleep(2)
            vectorstore = get_vectorstore(text_chunks)
            st.info(
                f"{st.session_state.username} your file's chunks are vectorized")
            t.sleep(2)
            status.update(label="Operation Completed!",
                          state="complete", expanded=False)
        st.session_state.conversation = get_conversation_chain(vectorstore)
        st.session_state.Processing = True
    if st.session_state.Processing:
        user_question = st.chat_input(
            f'{st.session_state.username} ask me anything from your given file')
        if user_question:
            handle_user_input(user_question)




def handle_user_input(user_question):
    """
    Handles the user input by making a conversation with the chatbot.

    Parameters:
        user_question (str): The question asked by the user.

    Returns:
        None
    """
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, messages in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", messages.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", messages.content), unsafe_allow_html=True)


if __name__ == '__main__':
    initialization()
    main()
