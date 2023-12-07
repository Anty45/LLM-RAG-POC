import re
from typing import List

from llama_index import Document


def remove_header(text: str) -> str:
    """
    Header always have "Grands arrêts - Petites fiches - 2017  p. PAGE_NB/PAGE_NB+1"
    we want to remove that
    :param text:
    :return:
    """
    text = text.replace("Grands arrêts - Petites fiches - 2017  p.", "")
    text = re.sub(r"[0-9]+/[0-9]+", "", text)
    text = text.strip()
    return text


def add_doc_section_to_metadata(document: Document) -> None:
    """
    Pass by reference where this document is located. Possible postions are :
    - introduction
    - arrets
    :param document:
    :return:
    """

    if int(document.metadata["page_label"]) < 11:
        document.metadata["section"] = "introduction"
    else:
        document.metadata["section"] = "arrets"


def clean_docs(docs: List[Document]) -> List[Document]:
    for doc in docs:
        doc.text = remove_header(doc.text)
        add_doc_section_to_metadata(doc)
    return docs
