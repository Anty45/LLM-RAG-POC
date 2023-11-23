from pathlib import Path
from llama_index import SimpleDirectoryReader


def load_documents(doc_path: Path):
    documents = SimpleDirectoryReader(str(doc_path)).load_data()
    return documents
