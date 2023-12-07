from pathlib import Path
from typing import List, Optional, Union

from llama_index import Document, SummaryIndex, VectorStoreIndex
from llama_index.chat_engine.types import BaseChatEngine
from llama_index.core import BaseQueryEngine

from src.llm_core.prompts import ZERO_SHOT_PROMPT


def instantiate_vector_summary_index(documents: List[Document], service_context):
    vector_index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    summary_index = SummaryIndex.from_documents(documents, service_context=service_context)
    return vector_index, summary_index


def store_index(vector_store: VectorStoreIndex, pth_vector_store: Path):
    vector_store.storage_context.persist(pth_vector_store)


def get_query_engine(
    vector_index, service_context, model_config
) -> Optional[Union[BaseQueryEngine, BaseChatEngine]]:
    if model_config["tasks"]["qa"]:
        query_engine = vector_index.as_query_engine(
            text_qa_template=ZERO_SHOT_PROMPT,
            service_context=service_context,
            streaming=True,
        )
    else:
        query_engine = vector_index.as_chat_engine(
            chat_mode=model_config["chat_mode"], verbose=True, streaming=True
        )

    return query_engine
