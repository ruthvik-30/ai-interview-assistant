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

        if docs:
            docs = self.reranker.rerank(query, docs)
            context = "\n\n".join([d.page_content for d in docs])
            prompt = f"""
            Use the context to answer the question.
            If not found, say you don't know.

            Context:
            {context}

            Question:
            {query}
            """
        else:
            # No relevant docs → just ask
            prompt = query

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
