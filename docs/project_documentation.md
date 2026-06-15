# Project Documentation

## Title

Agentic RAG-Based Enterprise Knowledge Assistant

## Objective

Build a capstone-ready Generative AI assistant that ingests enterprise documents, retrieves relevant evidence, and answers user questions using grounded RAG.

## Workflow

1. Upload supported files
2. Extract text per file format
3. Clean and chunk text
4. Generate sentence-transformer embeddings
5. Create FAISS index and metadata store
6. Retrieve evidence for a question
7. Generate an answer from retrieved context
8. Validate grounding and expose sources

## Reliability Controls

- File type validation
- Empty file detection
- Empty query handling
- Context sufficiency checks
- Grounding validation using lexical overlap
- Mock mode when no API key is present

## Design Notes

- The LLM layer is provider-oriented so another vendor can be added later
- Local embeddings keep the project usable without paid embedding APIs
- An offline hashing fallback keeps retrieval working when the sentence-transformer model is unavailable locally
- The agent workflow is intentionally simple and readable for academic review

## Challenges

- Converting tabular formats into QA-friendly text
- Keeping answers grounded instead of speculative
- Supporting both live LLM and offline demo behavior

## Suggested Demo Flow

1. Upload a small set of enterprise policies or reports
2. Ask a question that can be answered directly from the documents
3. Show the evidence chunks
4. Remove the API key and show that demo mode still performs retrieval
