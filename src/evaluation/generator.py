import pandas as pd
from llama_index.evaluation import DatasetGenerator
import random

from src.llm_core.prompts import ZERO_SHOT_PROMPT, ZERO_SHOT_QUESTION_PROMPT, ZERO_SHOT_QUESTION_TEMPLATE


def create_generator(nodes, context, questions_by_chunk, doc_nb) -> DatasetGenerator:
    data_generator = DatasetGenerator.from_documents(random.sample(nodes, doc_nb),
                                                     service_context=context,
                                                     num_questions_per_chunk=questions_by_chunk,
                                                     question_gen_query=ZERO_SHOT_QUESTION_TEMPLATE,
                                                     text_qa_template=ZERO_SHOT_PROMPT,
                                                     text_question_template= ZERO_SHOT_QUESTION_PROMPT,
                                                     show_progress=True)

    return data_generator


def generate_questions(generator: DatasetGenerator) -> pd.DataFrame:
    synthetic_questions = generator.generate_questions_from_nodes()
    return pd.DataFrame(
        {"questions": synthetic_questions},
    )
