# Execution Record

## Project Title

Agentic RAG-Based Enterprise Knowledge Assistant

## Purpose of This Record

This document is intended to provide verifiable evidence that the project was executed, tested, and reviewed as part of the capstone submission process. It should be submitted together with the source code, documentation, and screenshots.

## Execution Environment

- Operating System: Windows
- Programming Language: Python 3.10+
- Framework: Streamlit
- Vector Store: FAISS
- Embedding Layer: sentence-transformers or offline hashing fallback
- LLM Mode: OpenAI mode or mock demonstration mode

## Setup Commands Executed

Use the commands below as the official execution steps for the project:

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Test Command Executed

```bash
pytest
```

## Demo Dataset Used

The following public sample files are included with the project and may be used during demonstration:

- `data/sample_docs/employee_handbook.txt`
- `data/sample_docs/travel_policy.txt`
- `data/sample_docs/it_security_policy.txt`
- `data/sample_docs/quarterly_sales.csv`
- `data/sample_docs/training_records.xlsx`

## Example Questions Used During Execution

- What is the hotel reimbursement limit?
- How many remote work days are employees allowed per week?
- When must a security incident be reported?
- Which region had the highest revenue in Q2?
- Does the company require multi-factor authentication?

## Expected Execution Flow

1. Launch the Streamlit application.
2. Upload one or more files from `data/sample_docs`.
3. Click the document ingestion button.
4. Wait for the vector store and embedding pipeline to complete.
5. Enter a natural-language question in the chat input.
6. Review the generated answer and source evidence.
7. Run the test suite using `pytest`.

## Result Summary Template

Fill this section before final submission:

- Date of execution:
- System used:
- Python version:
- LLM mode used:
- Number of documents uploaded:
- Number of test cases passed:
- Overall execution status:

## Observed Outputs

Record a short summary of the observed behavior during execution:

- The application launched successfully.
- Documents were uploaded and ingested successfully.
- The vector store was created successfully.
- The system returned answers based on retrieved document evidence.
- Source chunks were displayed for verification.
- The test suite executed successfully.

## Screenshot Evidence

Attach the following screenshots in the `screenshots/` folder and reference them in the final submission:

- `home_page.png`
- `upload_success.png`
- `question_answer.png`
- `source_chunks.png`
- `test_results.png`

## Notes

- If `OPENAI_API_KEY` is not provided, the system operates in mock demonstration mode.
- Mock mode still demonstrates document ingestion, retrieval, and grounded response generation.
- This execution record can be updated with exact dates, versions, and screenshots before submission.

