"""
Scripts for evauate the RAG pipeline
"""
import sys
import pandas as pd
from pathlib import Path

from llama_index import set_global_service_context
from llama_index.node_parser import SimpleNodeParser

src_path = Path(__file__.split('src')[0])
sys.path.append(src_path.as_posix())

from src.utils.io import load_conf
from src.readers.loader import load_documents
from src.evaluation.generator import create_generator, generate_questions
from src.llm_core.llm import instantiate_llm, create_service_context
from src.llm_core.embbedings import create_embbeding


def run(path_conf: dict, model_conf: dict):

    law_docs = load_documents(src_path / path_conf["law_folder"])
    llm = instantiate_llm(model_conf, src_path / model_conf["llm_llama_path"])
    embbeding = create_embbeding(model_conf)
    service_context = create_service_context(llm, embbeding, model_conf)

    set_global_service_context(service_context)
    # Build index with a chunk_size of 512
    node_parser = SimpleNodeParser.from_defaults(chunk_size=211)
    nodes = node_parser.get_nodes_from_documents(law_docs)
    test_set_gen = create_generator(nodes,
                                    service_context,
                                    model_conf["chunk_questions_to_generate"],
                                    model_conf["doc_nb_for_eval"]
                                    )
    df_qa = generate_questions(test_set_gen)
    pth_to_qa_dataset = src_path / path_conf["test_set"] / "test_set.csv"
    if not Path(pth_to_qa_dataset).exists():
        Path(src_path / path_conf["test_set"]).mkdir(parents=True, exist_ok=True)
    df_qa.to_csv(
        src_path / path_conf["test_set"] / "test_set.csv",
        index=False
    )
    print("ok")
    #if not Path(path_conf["test_set"]).exists():






if __name__ == "__main__":
    path_pth = src_path / "conf/paths.yaml"
    mdl_pth = src_path / "conf/model.yaml"
    path_conf = load_conf(path_pth)
    mdl_conf = load_conf(mdl_pth)
    run(path_conf, mdl_conf)
