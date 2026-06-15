# Project Documentation

## Title

Agentic RAG-Based Enterprise Knowledge Assistant

## Objective

Build a capstone-ready Generative AI assistant that ingests enterprise documents, retrieves relevant evidence, and answers user questions using grounded RAG.

## System Architecture Diagram

The system architecture diagram is maintained in [architecture_diagram.md](./architecture_diagram.md).

Architecture summary:

1. The Streamlit UI handles document upload, ingestion status, question input, answer display, and source evidence display.
2. The ingestion pipeline loads PDF, TXT, CSV, XLSX, and XLS documents and converts them into normalized text.
3. The chunking layer splits text into overlapping segments suitable for semantic retrieval.
4. The embedding layer generates vector representations using a cached sentence-transformer model or an offline hashing fallback.
5. The FAISS vector store persists embeddings and metadata for similarity search.
6. The agent workflow plans retrieval, fetches relevant context, generates a grounded answer, and validates the result.
7. Guardrails enforce document-only answering and safe handling of weak or missing context.

## Agent Workflow

The project uses four simple agents with clearly separated responsibilities:

1. `PlannerAgent`
   Interprets the user question and creates a retrieval strategy.
2. `RetrieverAgent`
   Converts the question into an embedding, queries FAISS, and returns the top-k chunks.
3. `AnswerGeneratorAgent`
   Passes the retrieval plan and evidence into the RAG pipeline and calls the LLM layer.
4. `ValidatorAgent`
   Checks whether sources exist, whether retrieved context is strong enough, and whether the final answer appears grounded in the evidence.

End-to-end agent workflow:

1. The user submits a question from the UI.
2. Guardrails check for empty or invalid input.
3. The planner agent creates a retrieval plan.
4. The retriever agent gathers the most relevant document chunks.
5. The answer generator agent builds a context-constrained prompt.
6. The LLM provider returns either a live response or a mock demo response.
7. The validator agent verifies grounding before the answer is shown to the user.

## AI and UI Usage

### AI Usage

- Retrieval-Augmented Generation is used so answers are based on uploaded documents rather than open-ended model knowledge.
- Sentence-transformer embeddings are used by default for semantic retrieval.
- FAISS performs nearest-neighbor search over chunk embeddings.
- The LLM layer supports OpenAI through environment variables.
- If no API key is available, the application switches to mock demo mode while still using real retrieval results.
- The AI layer is modular, so another LLM provider can be added later with minimal changes.

### UI Usage

- The Streamlit interface provides a file uploader for supported enterprise documents.
- The sidebar shows key settings such as embedding model, LLM model, chunk size, and retrieval depth.
- Users ingest uploaded files before asking questions.
- Answers are displayed together with validation feedback and retrieved source chunks.
- The planner strategy can also be expanded in the UI for demonstration purposes.

## Limitations

- Character-based chunking is simpler than semantic or structure-aware chunking.
- Validation is heuristic and does not guarantee factual correctness in every case.
- Spreadsheet content is flattened into text, which may lose some structural meaning.
- Large document collections may require more scalable storage or background ingestion jobs.
- The offline hashing fallback is reliable for demos but less semantically rich than sentence-transformer embeddings.
- The app is designed for single-user local or classroom demonstration, not enterprise-scale production deployment.

## Assumptions

- Users upload documents that contain extractable text.
- Uploaded documents are relevant to the questions being asked.
- The local machine has enough memory and CPU resources for Streamlit, FAISS, and sentence-transformers.
- If OpenAI-based generation is desired, a valid `OPENAI_API_KEY` is available in the environment.
- The application is run in a trusted environment where local file uploads are acceptable.
- Retrieved context quality is generally sufficient when the source documents are clean and well-structured.

## Security Considerations

- The system is intentionally designed to answer only from uploaded documents.
- Unsupported file types are rejected before ingestion.
- Empty files, empty queries, and weak retrieval results are handled with explicit warnings.
- Environment variables are used for API keys so secrets are not hard-coded in source files.
- `.env`, uploaded documents, and vector index artifacts are excluded through `.gitignore`.
- The current project does not include authentication, authorization, encryption at rest, or document access controls.
- For real enterprise deployment, additional protections would be required:
  - user authentication
  - role-based access control
  - secure document storage
  - audit logging
  - rate limiting
  - network and secret management hardening

## Suggested Demo Flow

1. Upload a small set of enterprise policies or reports.
2. Ingest the files and explain the vectorization process.
3. Ask a question that can be answered directly from the uploaded documents.
4. Show the evidence chunks and validation result.
5. Demonstrate that the app refuses to answer confidently when context is insufficient.
