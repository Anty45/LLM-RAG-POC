import os
import openai
import sys

from typing import Dict
from pathlib import Path
from dotenv import load_dotenv
import logging

from llama_index import set_global_service_context


src_path = Path(__file__.split('src')[0])
sys.path.append(src_path.as_posix())

from src.utils.io import load_conf
from src.readers.loader import load_documents
from src.llm_core.indexing import instantiate_vector_summary_index, store_index
from src.llm_core.llm import instantiate_llm, create_service_context
from src.llm_core.embbedings import create_embbeding

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY


def run(model_config: Dict, data_paths: Dict, logger: logging):
    logger.info("LOAD DATA")
    law_docs = load_documents(src_path / data_paths["law_folder"])

    logger.info("INSTANTIATE LLM")
    llm = instantiate_llm(model_config, src_path / model_conf['llm_llama_path'])

    logger.info("EMBBEDING CREATION")
    embbeding = create_embbeding(model_config)
    service_context = create_service_context(llm, embbeding, model_config)

    set_global_service_context(service_context)

    pth_vector_store = Path(src_path / data_paths["vector_store"])
    if (pth_vector_store.exists() and len(os.listdir(pth_vector_store)) == 0) \
            or (not pth_vector_store.exists()) or model_config["force_indexing"]:  # if the path do not exists create it

        pth_vector_store.mkdir(exist_ok=True)

        logger.info("INDEXING")
        vector_index, summary_index = instantiate_vector_summary_index(law_docs, service_context)

        logger.info("STORE INDEX")
        store_index(vector_index, pth_vector_store)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger("llama")
    conf_path = src_path / "conf/model.yaml"
    data_path = src_path / "conf/paths.yaml"
    model_conf = load_conf(conf_path)
    data_conf = load_conf(data_path)

    run(model_conf, data_conf, logger)
