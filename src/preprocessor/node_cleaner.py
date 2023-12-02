import re
from typing import List
from llama_index import Document


def remove_header(text: str) -> str:
    text = text.replace("Grands arrêts - Petites fiches - 2017  p.", "")
    text = re.sub(r"[0-9]+/[0-9]+", "", text)
    text = text.strip()
    return text


def clean_docs(docs: List[Document]) -> List[Document]:
    for doc in docs:
        doc.text = remove_header(doc.text)
    return docs
