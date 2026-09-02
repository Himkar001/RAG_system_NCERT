from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

PERSIST_DIR = "chroma_db"

_embedding_model = None
_vectorstore = None
_parent_vectorstore = None

def load_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _embedding_model

def load_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        embedding_model = load_embedding_model()
        _vectorstore = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=embedding_model,
            collection_name="langchain"
        )
    return _vectorstore

def load_parent_vectorstore():
    global _parent_vectorstore
    if _parent_vectorstore is None:
        embedding_model = load_embedding_model()
        _parent_vectorstore = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=embedding_model,
            collection_name="parents"
        )
    return _parent_vectorstore