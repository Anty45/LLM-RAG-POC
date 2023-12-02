import pandas as pd
from llama_index.evaluation import DatasetGenerator
import random


def create_generator(nodes,
                     context,
                     questions_by_chunk,
                     doc_nb,
                     question_gen_query,
                     text_qa_template,
                     text_question_template) -> DatasetGenerator:
    data_generator = DatasetGenerator.from_documents(random.sample(nodes, doc_nb),
                                                     service_context=context,
                                                     num_questions_per_chunk=questions_by_chunk,
                                                     question_gen_query=question_gen_query,
                                                     text_qa_template=text_qa_template,
                                                     text_question_template=text_question_template,
                                                     show_progress=True)

    return data_generator


def generate_questions(generator: DatasetGenerator, prompt_used: str) -> pd.DataFrame:
    synthetic_questions = generator.generate_questions_from_nodes()
    return pd.DataFrame(
        {
            "questions": synthetic_questions,
            "prompt": prompt_used
        },
    )
