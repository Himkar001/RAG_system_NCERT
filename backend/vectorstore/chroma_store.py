from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


PERSIST_DIR = "chroma_db"


def load_embedding_model():

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embedding_model


def load_vectorstore():

    embedding_model = load_embedding_model()

    vectorstore = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embedding_model
    )

    return vectorstore