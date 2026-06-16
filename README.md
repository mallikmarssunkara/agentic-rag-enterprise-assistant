# Agentic RAG-Based Enterprise Knowledge Assistant

## Problem Statement

Enterprise knowledge is often distributed across heterogeneous document formats, including PDF files, plain text documents, spreadsheets, and tabular reports. This fragmentation makes timely and reliable information access difficult, particularly when users must manually locate relevant passages before making decisions. This project addresses that challenge by implementing a Retrieval-Augmented Generation (RAG) assistant that ingests uploaded enterprise documents, retrieves semantically relevant evidence, and generates responses constrained to the retrieved context.

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

## Project Objective

The objective of this capstone project is to design and implement a modular enterprise knowledge assistant that demonstrates the practical application of document ingestion, semantic retrieval, agent-based orchestration, grounded response generation, and reliability controls within a single end-to-end system.

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

## Prerequisites

Before running the application, ensure that the following are available:

- Python 3.10 or later
- `pip`
- Internet access if you want to use OpenAI responses or download the sentence-transformer model for the first time

## Setup and Run

### 1. Clone the repository

```bash
git clone https://github.com/Ravi-30/agetic-rag-assistant.git
cd agetic-rag-assistant
```

### 2. Create and activate a virtual environment

Detailed setup commands are also available in [setup_venv.md](./setup_venv.md).

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env`.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Then edit `.env` as needed:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=800
CHUNK_OVERLAP=150
TOP_K=4
```

Notes:

- If `OPENAI_API_KEY` is left empty, the application will still run in mock demo mode.
- Mock demo mode uses real retrieval from uploaded documents but does not call the OpenAI API.
- If the sentence-transformer model is not already cached locally, the project may use the offline hashing fallback for embeddings.

### 5. Start the application

```bash
streamlit run app.py
```

After startup, Streamlit will show a local URL, usually:

```text
http://localhost:8501
```

Open that address in your browser.

## How To Use the Application

1. Launch the Streamlit application.
2. Upload one or more files from `data/sample_docs/` or your own supported documents.
3. Click `Ingest Documents` to extract text, create chunks, generate embeddings, and build the FAISS index.
4. Enter a question in the chat input.
5. Review the generated answer, validation status, and retrieved source chunks.
6. Check the response mode shown in the interface:
   - `mock` means demo mode without OpenAI
   - `openai` means a real OpenAI API-backed response was used

## Run Tests

To verify the project setup, run:

```bash
pytest
```

If the setup is correct, the tests should complete successfully.

## Public Demo Data

The repository includes a small set of public demonstration documents in [data/sample_docs](./data/sample_docs) so the project can be evaluated without private enterprise data.

Included sample files:

- `employee_handbook.txt`
- `travel_policy.txt`
- `it_security_policy.txt`
- `quarterly_sales.csv`
- `training_records.xlsx`

Example prompts are provided in [docs/sample_queries.md](./docs/sample_queries.md).

Recommended first demo:

1. Upload all files from `data/sample_docs/`
2. Ingest the documents
3. Ask: `What is the hotel reimbursement limit?`
4. Ask: `How many remote work days are employees allowed per week?`

## Architecture

The system follows a modular RAG architecture composed of clearly separated processing layers:

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

## Documentation Coverage

The full project documentation in [docs/project_documentation.md](./docs/project_documentation.md) includes:

- System architecture diagram
- Agent workflow
- AI and UI usage
- Limitations
- Assumptions
- Security considerations

Additional submission support files are also included:

- [docs/execution_record.md](./docs/execution_record.md)
- [docs/submission_checklist.md](./docs/submission_checklist.md)
- [screenshots/README.md](./screenshots/README.md)

## Deployment Steps

1. Install dependencies in a virtual environment
2. Add environment variables
3. Run `streamlit run app.py`
4. Deploy to Streamlit Community Cloud, Render, or another Python hosting platform

## Limitations

- Character-based chunking is simpler than advanced semantic or structure-aware segmentation
- Validation is heuristic rather than a formal factual verification method
- Spreadsheet parsing converts structured data into plain text, which may reduce contextual fidelity
- Large document sets may require batching, persistent storage, or a more scalable retrieval backend

## Future Improvements

- Add hybrid retrieval with metadata filters
- Support citation highlighting in the answer body
- Add conversation memory for multi-turn QA
- Swap FAISS for a managed vector database
- Add authentication and document access control
