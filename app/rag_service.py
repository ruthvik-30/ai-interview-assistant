import time
from google import genai
from app.config import GEMINI_API_KEY
from app.retriever import HybridRetriever
from app.reranker import Reranker

client = genai.Client(api_key=GEMINI_API_KEY)

class RAGService:

    def __init__(self):
        self.retriever = HybridRetriever()
        self.reranker = Reranker()

    def generate(self, query):
        start = time.time()

        # Retrieve context
        docs = self.retriever.retrieve(query)

        if docs and len(docs)>0:
            docs = self.reranker.rerank(query, docs)
            context = "\n\n".join([d.page_content for d in docs])
            prompt = f"""
            You are a helpful AI assistant.

            Use the provided context to answer the question.
            If the context is insufficient, you may use your own knowledge.

            Context:
            {context}

            Question:
            {query}
            """
        else:
            # No relevant docs → just ask
            prompt = f"""
            You are an expert technical interviewer.

            Answer the question clearly with:
            - Definition
            - Key points
            - Example (if applicable)

            Do NOT say "I don't know".

            Question:
            {query}
            """

        # Generate text
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        latency = round(time.time() - start, 2)
        return {
            "answer": response.text,
            "latency_seconds": latency
        }
