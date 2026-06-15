# Architecture Overview

The application follows a modular architecture intended to demonstrate the principal components of an enterprise Retrieval-Augmented Generation system in a form that is clear, testable, and appropriate for a capstone submission.

1. Users upload enterprise documents through Streamlit.
2. The document loader extracts normalized text from PDF, TXT, CSV, XLSX, and XLS files.
3. A text chunker creates overlapping chunks for semantic retrieval.
4. Local sentence-transformer embeddings are generated for each chunk.
5. FAISS stores vectors for fast similarity search.
6. A lightweight agent workflow plans retrieval, fetches evidence, generates an answer, and validates grounding.
7. Guardrails ensure the app refuses unsupported files, empty input, and ungrounded answers.

Primary components:

- `app.py`: Streamlit interface and workflow orchestration
- `src/document_loader.py`: File parsing and text extraction
- `src/text_chunker.py`: Chunking logic
- `src/embeddings.py`: Embedding model wrapper
- `src/vector_store.py`: FAISS indexing and search
- `src/llm.py`: OpenAI and mock LLM providers
- `src/rag_pipeline.py`: Prompt assembly and grounded answering
- `src/agents.py`: Planner, Retriever, Answer Generator, Validator
- `src/guardrails.py`: Validation and safety checks

See the full Mermaid diagram in [docs/architecture_diagram.md](./docs/architecture_diagram.md). The architecture is organized into the following layers:

- Ingestion: upload, parse, clean, chunk, embed, index
- Query handling: validate, plan, retrieve, generate, validate again
- Storage: uploaded files and FAISS vector index metadata
