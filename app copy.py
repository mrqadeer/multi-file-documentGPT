import streamlit as st
from streamlit_chat import message
from streamlit_option_menu import option_menu
import os

from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain import HuggingFaceHub
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import get_openai_callback
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
from docx import Document
import time as t
import tempfile
from langchain.document_loaders.csv_loader import CSVLoader

from templates.htmlTemplates import css, bot_template, user_template


def Initial():
    st.set_page_config(page_title='Document Master',
                       page_icon=':books:', initial_sidebar_state='collapsed')
    st.title('Document Chatbot by Qadeer')
    global data
    data = ['Sir Irfan Malik', 'Hope To Skill',
            'Artificial Intelligence Course']
    for name in data:
        st.subheader(name, divider='rainbow')


def main():
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
            files_text = GetFileText(uploaded_files)
            st.info(f'{st.session_state.username} your file(s) loaded')
            st.write("Making Chunks")
            t.sleep(2)
            text_chunks = GetFileChunks(files_text)
            st.info(f"{st.session_state.username} your file's chunks are created")
            st.write("Vectorizing Chunks")
            t.sleep(2)
            vectorstore = GetVectorStore(text_chunks)
            st.info(
                f"{st.session_state.username} your file's chunks are vectorized")
            t.sleep(2)
            status.update(label="Operation Completed!",
                          state="complete", expanded=False)
        st.session_state.conversation = GetConversationChain(vectorstore)
        st.session_state.Processing = True
    if st.session_state.Processing:
        user_question = st.chat_input(
            f'{st.session_state.username} ask me anything from your given file')
        if user_question:
            HandleUserInput(user_question)

# Defining Functions


def GetFileText(uploaded_files):
    text = ""
    for uploaded_file in uploaded_files:
        split_up = os.path.splitext(uploaded_file.name)
        file_extension = split_up[1]
        if file_extension == '.pdf':
            text += GetPDFText(uploaded_file)
        elif file_extension == '.docx':
            text += GetDocxText(uploaded_file)
        else:
            st.stop()
    return text
# GetFileText Nested Functions


def GetPDFText(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def GetDocxText(file):
    documemt = Document(file)
    AllText = []
    for document_paragraph in documemt.paragraphs:
        AllText.append(document_paragraph.text)
    text = " ".join(AllText)
    return text


def GetCSVFile(uploaded_file, work_file):
    if work_file == 'Tabular':
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

        loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={
            'delimiter': ','})
        data = loader.load()


def GetFileChunks(file):
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=900,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(file)
    # st.write(chunks)
    return chunks


def GetVectorStore(text_chunks):
    embedding = HuggingFaceEmbeddings(
        model_name=st.session_state.embedding_model)

    # embedding = OpenAIEmbeddings(openai_api_key=st.session_state.api_key)
    knowledge_base = FAISS.from_texts(text_chunks, embedding)
    return knowledge_base


def GetConversationChain(vectprstore):
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


def HandleUserInput(user_question):
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
    Initial()
    main()
