import sys
from pathlib import Path
from typing import Dict

import pytest

root_path = Path(__file__.split("tests")[0])
sys.path.append(root_path.as_posix())

from src.preprocessor.node_cleaner import (  # noqa
    add_doc_section_to_metadata,
    remove_header,
)


class LawDocument:
    def __init__(self, text: str, metadata: Dict):
        self.text = text
        self.metadata = metadata


@pytest.fixture()
def intro():
    return LawDocument(
        "   Grands arrêts - Petites fiches - 2017  p.  azerty test",
        {"page_label": 5},
    )


@pytest.fixture()
def arret():
    return LawDocument(" azerty ", {"page_label": 12})


def test_remove_header_intro(intro):
    data_text = intro.text
    assert remove_header(data_text) == "azerty test"


def test_add_doc_section_to_metadata_intro(intro):
    add_doc_section_to_metadata(intro)
    assert "section" in intro.metadata
    assert intro.metadata["section"] == "introduction"


def test_remove_header_arret(arret):
    arret_text = arret.text
    assert remove_header(arret_text) == "azerty"


def test_add_doc_section_to_metadata_arret(arret):
    add_doc_section_to_metadata(arret)
    assert "section" in arret.metadata
    assert arret.metadata["section"] == "arrets"
