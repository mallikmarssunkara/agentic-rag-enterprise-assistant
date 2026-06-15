# Agentic RAG-Based Enterprise Knowledge Assistant

## Problem Statement

Enterprise teams often store critical knowledge across multiple document formats. Finding reliable answers quickly becomes difficult when information is spread across PDFs, text files, spreadsheets, and tables. This project solves that problem with a Retrieval-Augmented Generation application that only answers from uploaded business documents.

## Features

- Upload PDF, TXT, CSV, XLSX, and XLS documents
- Extract and clean document text
- Split content into overlapping semantic chunks
- Generate local embeddings using sentence-transformers
- Fall back to a deterministic offline hashing embedder if the transformer model is not cached locally
- Index and search chunks with FAISS
- Run an agentic workflow with planner, retriever, answer generator, and validator agents
- Show retrieved source chunks as evidence
- Enforce guardrails for empty queries, unsupported files, insufficient context, and ungrounded answers
- Support OpenAI for live LLM responses with a mock demo mode fallback

## Tech Stack

- Python 3.10+
- Streamlit
- sentence-transformers
- FAISS
- OpenAI API
- pandas
- pypdf
- openpyxl
- python-dotenv

## Folder Structure

```text
agentic-rag-enterprise-assistant/
|-- app.py
|-- requirements.txt
|-- .env.example
|-- .gitignore
|-- README.md
|-- setup_venv.md
|-- architecture.md
|-- src/
|-- data/
|-- docs/
|-- tests/
`-- screenshots/
```

## Setup Instructions

1. Create a virtual environment by following [setup_venv.md](./setup_venv.md).
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env`.
4. Add an `OPENAI_API_KEY` if you want live LLM answers.
5. Launch the app with `streamlit run app.py`.

## How To Use

1. Open the Streamlit app.
2. Upload one or more supported documents.
3. Click the ingestion button to build the vector store.
4. Ask a question in natural language.
5. Review the grounded answer, validation status, and retrieved source chunks.

## Architecture

The solution uses a modular RAG pipeline:

- Document ingestion normalizes raw files into text records.
- Text chunking creates overlapping segments for retrieval quality.
- Local embeddings are created with `all-MiniLM-L6-v2`.
- If that model is not already cached on the machine, the app falls back to an offline hashing embedder so retrieval still works.
- FAISS performs top-k semantic similarity search.
- The agent workflow plans retrieval, gathers context, drafts an answer, and validates grounding.

More detail is available in [architecture.md](./architecture.md) and [docs/project_documentation.md](./docs/project_documentation.md).

## Agent Roles

- `PlannerAgent`: Interprets the question and decides the retrieval approach
- `RetrieverAgent`: Searches the vector store for the most relevant chunks
- `AnswerGeneratorAgent`: Uses RAG context to generate the final response
- `ValidatorAgent`: Confirms that the answer is grounded in retrieved evidence

## RAG Workflow

1. Upload and parse files
2. Clean and chunk text
3. Generate embeddings
4. Build FAISS index
5. Retrieve top-k chunks for a query
6. Prompt the LLM with only retrieved context
7. Validate evidence coverage before showing the result

## Safety Controls

- Unsupported files are rejected before ingestion
- Empty files and empty queries return clear warnings
- Low-context retrieval triggers a "not found in documents" response
- Source chunks are always displayed
- Mock mode works without an API key while remaining grounded in retrieved text

## Deployment Steps

1. Install dependencies in a virtual environment
2. Add environment variables
3. Run `streamlit run app.py`
4. Deploy to Streamlit Community Cloud, Render, or another Python hosting platform

## Limitations

- Character-based chunking is simpler than advanced semantic chunking
- Validation is heuristic rather than formal factual verification
- Spreadsheet parsing converts structured data into plain text
- Large document sets may need batching or persistent databases for scale

## Future Improvements

- Add hybrid retrieval with metadata filters
- Support citation highlighting in the answer body
- Add conversation memory for multi-turn QA
- Swap FAISS for a managed vector database
- Add authentication and document access control
