# Architecture Overview

The application follows a simple production-style flow:

1. Users upload enterprise documents through Streamlit.
2. The document loader extracts normalized text from PDF, TXT, CSV, XLSX, and XLS files.
3. A text chunker creates overlapping chunks for semantic retrieval.
4. Local sentence-transformer embeddings are generated for each chunk.
5. FAISS stores vectors for fast similarity search.
6. A lightweight agent workflow plans retrieval, fetches evidence, generates an answer, and validates grounding.
7. Guardrails ensure the app refuses unsupported files, empty input, and ungrounded answers.

Components:

- `app.py`: Streamlit interface and workflow orchestration
- `src/document_loader.py`: File parsing and text extraction
- `src/text_chunker.py`: Chunking logic
- `src/embeddings.py`: Embedding model wrapper
- `src/vector_store.py`: FAISS indexing and search
- `src/llm.py`: OpenAI and mock LLM providers
- `src/rag_pipeline.py`: Prompt assembly and grounded answering
- `src/agents.py`: Planner, Retriever, Answer Generator, Validator
- `src/guardrails.py`: Validation and safety checks

See the full Mermaid diagram in [docs/architecture_diagram.md](./docs/architecture_diagram.md). It is structured into:

- Ingestion: upload, parse, clean, chunk, embed, index
- Query handling: validate, plan, retrieve, generate, validate again
- Storage: uploaded files and FAISS vector index metadata
