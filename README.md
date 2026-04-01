# Gemini AI Interview Assistant

A retrieval-augmented generation (RAG) project that combines a FastAPI backend, Streamlit frontend, hybrid search, and Google Gemini AI to generate interview questions, evaluate answers, and provide feedback.

## Features

- **Mock interview generation**: Generate interview questions by topic using Gemini AI.
- **Answer evaluation**: Score candidate answers on correctness, depth, and clarity, then provide improvement suggestions.
- **Hybrid retrieval**: Use FAISS embeddings and BM25 sparse search to retrieve relevant documents from technical Q&A and code snippets.
- **Reranking**: Improve result quality with a cross-encoder reranker.
- **Streamlit UI**: Simple frontend for asking questions and performing mock interviews.

## Tech Stack

- Python
- FastAPI
- Streamlit
- Google Gemini AI (`google-genai`)
- LangChain / `langchain-community`
- FAISS
- HuggingFace embeddings (`sentence-transformers/all-MiniLM-L6-v2`)
- Sentence Transformers cross-encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`)
- BM25 retrieval (`rank-bm25`)
- `python-dotenv`
- `pydantic`

## Repository Structure

- `app/`
  - `main.py` - FastAPI server with endpoints for asking questions, generating mock questions, and evaluating answers.
  - `rag_service.py` - Gemini model integration and prompt generation.
  - `interview_service.py` - Question generation and answer evaluation logic.
  - `ingest.py` - Data ingestion and vectorstore building.
  - `retriever.py` - Hybrid retriever combining FAISS and BM25.
  - `reranker.py` - Cross-encoder reranking for retrieved documents.
  - `config.py` - Environment configuration.
- `frontend/`
  - `streamlit_app.py` - Streamlit app for the UI.
- `codebase/` - Example code files ingested into the knowledge base.
- `data/` - Technical interview Q&A data.
- `vectorstore/` - Local FAISS vectorstore storage.
- `requirements.txt` - Python dependencies.

## Setup

1. Create and activate the Python virtual environment:

   ```bash
   python -m venv aipro
   .\aipro\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:

   - Create a `.env` file in the root directory.
   - Add your Gemini API key:

     ```env
     GEMINI_API_KEY=your_api_key_here
     ```

4. Build the vectorstore (optional if already generated):

   ```bash
   python app\ingest.py
   ```

## Running the App

### Start the backend API

```bash
uvicorn app.main:app --reload
```

### Start the Streamlit frontend

```bash
streamlit run frontend\streamlit_app.py
```

The Streamlit UI will connect to the backend at `http://localhost:8000` by default.

## Usage

- Use the **Ask Assistant** mode to query the AI assistant for DSA, ML, or coding-related questions.
- Use the **Mock Interview** mode to generate interview questions by topic, enter your answer, and receive an evaluation.

## Notes

- The project uses a local FAISS vectorstore stored under `vectorstore/`.
- The retriever ingests both the Q&A dataset and Python code from the `codebase/` folder.
- Evaluation results are generated via Gemini AI and may require prompt tuning for more consistent JSON output.

## License

This project is provided as-is for learning and demo purposes.
