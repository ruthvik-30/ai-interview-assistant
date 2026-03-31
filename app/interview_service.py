import json, re
from app.rag_service import RAGService

rag = RAGService()

def generate_question(topic):
    prompt = f"Generate an interview question on {topic} with category and difficulty."
    result = rag.generate(prompt)
    return {"answer": result["answer"], "latency_seconds": result["latency_seconds"]}



def evaluate_answer(question, answer):
    if not answer.strip():
        return {
            "score": {"Correctness": 0, "Depth": 0, "Clarity": 0},
            "feedback": "Short or No answer provided. Please attempt the question.",
            "improved_answer": ""
        }

    prompt = f"""
    Evaluate the candidate answer and return valid JSON only:

    Question: {question}
    Answer: {answer}

    Return JSON like:
    {{
      "score": {{
        "Correctness": 0-10,
        "Depth": 0-10,
        "Clarity": 0-10
      }},
      "feedback": "Improvement suggestions",
      "improved_answer": "Better answer"
    }}
    """
    response = rag.generate(prompt)
    text = response.get("answer", "")

    # Try extracting JSON from model text
    import re, json
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass

    # fallback if model fails or returns invalid JSON
    return {
        "score": {"Correctness": 0, "Depth": 0, "Clarity": 0},
        "feedback": "Could not generate proper evaluation. Try rephrasing your answer.",
        "improved_answer": ""
    }
