"""
This is a core class of the package holdings all routes of QA service
"""
from fastapi import APIRouter, Request, Depends
from src.serving.qa.schemas import Question

qa_router = APIRouter(
    prefix="/qa",
    tags=[""],
    responses={404: {"description": "ressource-not-found"}}
)


@qa_router.get("/{question}")
def question_answering(request: Request, question: Question = Depends()):
    query_engine = request.state.query_engine
    if question.text is None or question.text.strip() == "":
        return {"answer": "Ask a question"}
    answer = query_engine.query(question.text)
    return {"answer": answer.print_response_stream()}
