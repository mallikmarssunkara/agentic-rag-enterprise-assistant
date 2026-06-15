# Architecture Diagram

```mermaid
flowchart TD
    U["User"] --> UI["Streamlit Interface<br/>app.py"]

    subgraph INGEST["Document Ingestion Pipeline"]
        UI --> UP["File Upload<br/>PDF / TXT / CSV / XLSX / XLS"]
        UP --> DL["Document Loader<br/>document_loader.py"]
        DL --> CT["Text Cleaning"]
        CT --> CH["Chunking Engine<br/>text_chunker.py"]
        CH --> EM["Embedding Service<br/>sentence-transformers or hashing fallback"]
        EM --> VS["FAISS Vector Store<br/>index.faiss + metadata.json"]
    end

    subgraph QUERY["Question Answering Pipeline"]
        UI --> Q["User Question"]
        Q --> GR1["Guardrails<br/>empty query / unsupported input"]
        GR1 --> PA["Planner Agent"]
        PA --> RA["Retriever Agent"]
        RA --> QE["Query Embedding"]
        QE --> VS
        VS --> RC["Top-K Retrieved Chunks"]
        RC --> AA["Answer Generator Agent"]
        AA --> RAG["RAG Prompt Builder<br/>rag_pipeline.py"]
        RAG --> LLM["LLM Layer<br/>OpenAI or Mock Demo Mode"]
        RC --> VA["Validator Agent"]
        LLM --> OUT["Grounded Answer"]
        VA --> OUT
        OUT --> GR2["Final Validation<br/>context sufficiency / groundedness"]
        GR2 --> UI
    end

    subgraph STORAGE["Project Storage"]
        FILES["data/uploaded_docs/"]
        INDEX["data/vector_store/"]
    end

    UP --> FILES
    VS --> INDEX
```

## Diagram Notes

- The ingestion pipeline converts uploaded enterprise documents into searchable chunks.
- The vector store keeps both embeddings and chunk metadata for retrieval.
- The agent layer separates planning, retrieval, answer generation, and validation.
- Guardrails run before and after generation to keep answers document-grounded.
