from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_service import RAGService
from app.interview_service import generate_question, evaluate_answer

app = FastAPI()
rag = RAGService()


class Query(BaseModel):
    query: str


class InterviewRequest(BaseModel):
    topic: str


class EvaluationRequest(BaseModel):
    question: str
    answer: str


@app.post("/ask")
def ask(data: Query):
    try:
        result = rag.generate(data.query)
        return result
    except Exception as e:
        return {"error": str(e)}


@app.post("/mock-question")
def mock(data: InterviewRequest):
    try:
        return generate_question(data.topic)
    except Exception as e:
        return {"error": str(e)}


@app.post("/evaluate")
def evaluate(data: EvaluationRequest):
    try:
        return evaluate_answer(data.question, data.answer)
    except Exception as e:
        return {"error": str(e)}