from pathlib import Path
from typing import List

from llama_index import Document, SimpleDirectoryReader
from llama_index.node_parser import SimpleNodeParser
from llama_index.schema import BaseNode


def load_documents(doc_path: Path) -> list[Document]:
    documents = SimpleDirectoryReader(str(doc_path)).load_data()
    return documents


def build_nodes(docs: List[Document], node_chunk_size: int) -> List[BaseNode]:
    node_parser = SimpleNodeParser.from_defaults(chunk_size=node_chunk_size)
    nodes = node_parser.get_nodes_from_documents(docs)
    return nodes
