from __future__ import annotations

from pathlib import Path

import streamlit as st

from src.app_bootstrap import build_assistant
from src.config import get_settings
from src.document_loader import DocumentLoader
from src.guardrails import validate_file_type
from src.text_chunker import TextChunker
from src.utils import ensure_directory, format_score, save_uploaded_file

st.set_page_config(page_title="Enterprise Knowledge Assistant", layout="wide")


def ingest_documents(uploaded_files) -> dict:
    settings = get_settings()
    ensure_directory(settings.upload_dir)
    ensure_directory(settings.vector_store_dir)

    saved_paths: list[Path] = []
    warnings: list[str] = []

    for uploaded_file in uploaded_files:
        file_warning = validate_file_type(uploaded_file.name, settings.supported_extensions)
        if file_warning:
            warnings.append(file_warning)
            continue
        saved_paths.append(save_uploaded_file(uploaded_file, settings.upload_dir))

    loader = DocumentLoader(settings.supported_extensions)
    documents, load_errors = loader.load_files(saved_paths)
    warnings.extend(load_errors)

    if not documents:
        return {"success": False, "warnings": warnings or ["No valid documents were ingested."]}

    chunker = TextChunker(settings.chunk_size, settings.chunk_overlap)
    chunks = chunker.chunk_documents(documents)
    assistant, embedding_service, vector_store = build_assistant(settings)
    embeddings = embedding_service.embed_documents([chunk["text"] for chunk in chunks])
    vector_store.build(chunks, embeddings)

    st.session_state["assistant"] = assistant
    st.session_state["ingested"] = True
    st.session_state["embedding_backend"] = embedding_service.backend

    return {
        "success": True,
        "warnings": warnings,
        "document_count": len(documents),
        "chunk_count": len(chunks),
        "embedding_backend": embedding_service.backend,
    }


def get_assistant():
    settings = get_settings()
    current_key = st.session_state.get("current_openai_api_key", None)
    if "assistant" not in st.session_state or settings.openai_api_key != current_key:
        assistant, embedding_service, vector_store = build_assistant(settings)
        vector_store.load()
        st.session_state["assistant"] = assistant
        st.session_state["embedding_backend"] = embedding_service.backend
        st.session_state["current_openai_api_key"] = settings.openai_api_key
    return st.session_state["assistant"]


def main() -> None:
    settings = get_settings()
    st.title("Agentic RAG-Based Enterprise Knowledge Assistant")
    st.caption("Upload enterprise documents, retrieve relevant evidence, and generate grounded answers.")

    with st.sidebar:
        st.header("Settings")
        user_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.get("OPENAI_API_KEY", settings.openai_api_key),
            type="password",
            placeholder="sk-...",
        )
        if user_key != st.session_state.get("OPENAI_API_KEY", settings.openai_api_key):
            st.session_state["OPENAI_API_KEY"] = user_key
            st.rerun()

        st.write(f"Embedding model: `{settings.embedding_model}`")
        st.write(f"OpenAI model: `{settings.openai_model}`")
        st.write(f"Chunk size: `{settings.chunk_size}`")
        st.write(f"Chunk overlap: `{settings.chunk_overlap}`")
        st.write(f"Top-k retrieval: `{settings.top_k}`")
        st.info(
            "If `OPENAI_API_KEY` is not set, the app switches to demo mode and summarizes retrieved evidence."
        )

    uploaded_files = st.file_uploader(
        "Upload PDF, TXT, CSV, XLSX, or XLS files",
        type=["pdf", "txt", "csv", "xlsx", "xls"],
        accept_multiple_files=True,
    )

    if st.button("Ingest Documents", type="primary"):
        if not uploaded_files:
            st.warning("Please upload at least one supported document.")
        else:
            with st.spinner("Extracting text, chunking content, and building the FAISS index..."):
                result = ingest_documents(uploaded_files)
            if result["success"]:
                st.success(
                    f"Ingestion complete. Loaded {result['document_count']} document records and created {result['chunk_count']} chunks."
                )
                st.info(f"Embedding backend used: `{result['embedding_backend']}`")
            else:
                st.error("Document ingestion did not complete successfully.")
            for warning in result.get("warnings", []):
                st.warning(warning)

    question = st.chat_input("Ask a question about the uploaded documents")
    if question:
        assistant = get_assistant()
        try:
            with st.spinner("Planner, retriever, generator, and validator agents are working..."):
                response = assistant.ask(question)
            st.subheader("Generated Answer")
            st.write(response["answer"])

            validation = response.get("validation", {})
            if validation.get("is_valid"):
                st.success("Validation status: grounded in retrieved evidence.")
            else:
                for warning in validation.get("warnings", []):
                    st.warning(warning)

            st.subheader("Retrieved Source Chunks")
            if response.get("sources"):
                for index, source in enumerate(response["sources"], start=1):
                    with st.expander(
                        f"Source {index}: {source['source']} (score: {format_score(source['score'])})"
                    ):
                        st.caption(str(source["metadata"]))
                        st.write(source["text"])
            else:
                st.info("No source chunks were returned.")

            if response.get("plan"):
                with st.expander("Planner Agent Strategy"):
                    st.text(response["plan"])

            st.caption(f"Response mode: {response.get('mode', 'unknown')}")
            if "embedding_backend" in st.session_state:
                st.caption(f"Embedding backend: {st.session_state['embedding_backend']}")
        except Exception as exc:
            st.error(f"An error occurred while answering the question: {exc}")


if __name__ == "__main__":
    main()
