from llama_index.prompts import PromptTemplate

ZERO_SHOT_QA_TEMPLATE = (
    "<|system|>: Reponds à une question à partir du contexte en français.\n"
    "<|user|>: {query_str} {context_str} \n"
    "<|Réponse|>:"
)

ZERO_SHOT_PROMPT = PromptTemplate(ZERO_SHOT_QA_TEMPLATE)

ZERO_SHOT_QUESTION_TEMPLATE = (
    """
    <|system|>: Génère une question brève à partir du contexte suivant en français.\n
    <|user|>: {context_str}\n
    <|Question|>:
    """
)

ZERO_SHOT_QUESTION_PROMPT = PromptTemplate(ZERO_SHOT_QUESTION_TEMPLATE)

FEW_SHOT_QUESTION_PROMPT = (
    """
    
    <|system|>: Génère une question brève à partir du contexte suivant en français.\n
    <|user|>: {context_str}\n
    <|Question|>:
    """
)
