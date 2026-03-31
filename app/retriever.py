from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.ingest import load_documents
from app.config import VECTOR_PATH


class HybridRetriever:

    def __init__(self):
        documents = load_documents()
        # documents can be list of strings

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Load FAISS vectorstore
        self.vectorstore = FAISS.load_local(
            VECTOR_PATH,
            self.embeddings,
            allow_dangerous_deserialization=True
        )

        # BM25 sparse retriever
        self.sparse = BM25Retriever.from_documents(documents)
        self.sparse.k = 5

    def retrieve(self, query):
        # dense (FAISS) retrieval
        dense_docs = self.vectorstore.similarity_search(query, k=5)

        # sparse (BM25) retrieval
        sparse_docs = self.sparse.invoke(query)

        # Convert all items to dict with page_content safely
        safe_docs = []

        for doc in dense_docs + sparse_docs:
            # If it's already a dict or object with page_content
            if hasattr(doc, "page_content"):
                safe_docs.append(doc)
            else:
                # if it’s a string, wrap in an object with page_content
                class TempDoc:
                    def __init__(self, content):
                        self.page_content = content
                safe_docs.append(TempDoc(str(doc)))

        # Deduplicate by content
        combined = {d.page_content: d for d in safe_docs}
        return list(combined.values())


# Quick test
if __name__ == "__main__":
    retriever = HybridRetriever()
    docs = retriever.retrieve("Explain time vs space complexity")
    for d in docs:
        print(d.page_content)
