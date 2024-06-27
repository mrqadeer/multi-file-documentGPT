# Multi-File Document Chatbot

![Document Master](https://img.shields.io/badge/Document-Master-brightgreen)
#### Check it out: [Streamlit App](https://mrqadeer-multi-file-documentgpt-app-zzm3ie.streamlit.app/)

## Overview

**Document Master** is an advanced multi-file chatbot designed to facilitate interaction with PDF and MS Word documents. Leveraging OpenAI with LangChain and Hugging Face embedding models, this chatbot can handle questions from multiple documents simultaneously. 

## Key Features

- **Multi-File Support**: Upload and process multiple PDF and DOCX files concurrently.
- **Advanced Embeddings**: Choose from several Hugging Face embedding models (`all-MiniLM-L6-v2`, `bert-base-uncased`, `bert-large-uncased`, `roberta-base`) to vectorize document chunks.
- **Interactive Chat**: Ask questions related to your uploaded documents and receive precise answers.
- **Streamlit Integration**: A user-friendly interface built with Streamlit for easy interaction.

## Setup

### Prerequisites

- Python 3.8+
- An OpenAI API Key

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/mrqadeer/multi-file-documentGPT.git
    cd multi-file-documentGPT
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```
### Running the Application

1. **Start the Streamlit app**:
    ```sh
    streamlit run app.py
    ```

2. **Interact with the Chatbot**:
    - Enter your name and OpenAI API key.
    - Set the desired temperature for the language model.
    - Choose your embedding model.
    - Upload your PDF and DOCX files.
    - Ask questions and get answers from your documents.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to:
- **Sir Irfan Malik** for his guidance and support.
- **Hope To Skill** for providing resources.
- **Artificial Intelligence Course** for the foundational knowledge.

## Contact

For any questions or suggestions, please feel free to reach out to me via [GitHub Issues](https://github.com/mrqadeer/multi-file-documentGPT/issues).

---

Happy Document Chatting!
