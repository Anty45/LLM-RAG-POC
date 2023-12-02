"""
Scripts for evauate the RAG pipeline
"""
import sys
from pathlib import Path

import pandas as pd
from llama_index import set_global_service_context


src_path = Path(__file__.split('src')[0])
sys.path.append(src_path.as_posix())

from src.utils.io import load_conf
from src.readers.loader import load_documents, build_nodes
from src.evaluation.generator import create_generator, generate_questions
from src.llm_core.llm import instantiate_llm, create_service_context
from src.llm_core.embbedings import create_embbeding
from src.llm_core.prompts import ZERO_SHOT_PROMPT, ZERO_SHOT_QUESTION_PROMPT, ZERO_SHOT_QUESTION_TEMPLATE
from src.preprocessor.node_cleaner import clean_docs


def run(path_conf: dict, model_conf: dict):

    # Format data
    law_docs = load_documents(src_path / path_conf["law_folder"])
    law_docs_cleaned = clean_docs(law_docs)
    nodes = build_nodes(law_docs_cleaned, model_conf["node_chunk_size"])

    # Instantiate llm
    llm = instantiate_llm(model_conf, src_path / model_conf["llm_llama_path"])
    embbeding = create_embbeding(model_conf)
    service_context = create_service_context(llm, embbeding, model_conf)
    set_global_service_context(service_context)

    # Generate context question pairs
    test_set_gen = create_generator(nodes,
                                    service_context,
                                    model_conf["chunk_questions_to_generate"],
                                    model_conf["doc_nb_for_eval"],
                                    ZERO_SHOT_QUESTION_TEMPLATE,
                                    ZERO_SHOT_PROMPT,
                                    ZERO_SHOT_QUESTION_PROMPT
                                    )
    df_qa = generate_questions(test_set_gen, ZERO_SHOT_QUESTION_TEMPLATE)

    # Save
    pth_qa_folder = src_path / path_conf["test_set"]
    pth_to_qa_dataset = src_path / path_conf["test_set"] / "test_set.csv"

    if not Path(pth_qa_folder).exists():
        Path(src_path / path_conf["test_set"]).mkdir(parents=True, exist_ok=True)

    if Path(pth_to_qa_dataset).exists() and not model_conf["start_qa_pair_gen"]:
        df_qa_existing = pd.read_csv(pth_to_qa_dataset)
        df_qa = pd.concat([df_qa, df_qa_existing], axis=0)

    df_qa.to_csv(
        src_path / path_conf["test_set"] / path_conf["test_set_name"],
        index=False
    )


if __name__ == "__main__":
    path_pth = src_path / "conf/paths.yaml"
    mdl_pth = src_path / "conf/model.yaml"
    path_conf = load_conf(path_pth)
    mdl_conf = load_conf(mdl_pth)
    run(path_conf, mdl_conf)
