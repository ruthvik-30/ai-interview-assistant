from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):
        self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def rerank(self, query, docs):
        pairs = [(query, doc.page_content) for doc in docs]
        scores = self.model.predict(pairs)

        ranked = list(zip(docs, scores))
        ranked.sort(key=lambda x: x[1], reverse=True)

        return [doc for doc, _ in ranked[:5]]
