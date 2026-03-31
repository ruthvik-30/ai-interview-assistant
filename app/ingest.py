import json
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import VECTOR_PATH


def load_documents():
    docs = []

    # Load JSON Q&A
    with open("data/interview_qa.json", "r") as f:
        data = json.load(f)

    for item in data:
        content = f"""
        Category: {item['category']}
        Difficulty: {item['difficulty']}
        Question: {item['question']}
        Answer: {item['answer']}
        """
        docs.append(Document(page_content=content))

    # Load codebase
    for root, _, files in os.walk("codebase"):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r") as f:
                    docs.append(Document(page_content=f.read()))

    return docs


def build_vectorstore():
    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    split_docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(split_docs, embeddings)
    vectorstore.save_local(VECTOR_PATH)

    print("Vectorstore built successfully.")


if __name__ == "__main__":
    build_vectorstore()
