from pathlib import Path

from llama_index import SimpleDirectoryReader, Document
from llama_index.node_parser import SimpleNodeParser


def load_documents(doc_path: Path) -> list[Document]:
    documents = SimpleDirectoryReader(str(doc_path)).load_data()
    return documents


def build_nodes(docs, node_chunk_size: int):
    node_parser = SimpleNodeParser.from_defaults(chunk_size=node_chunk_size)
    nodes = node_parser.get_nodes_from_documents(docs)
    return nodes
