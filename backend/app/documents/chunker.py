from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.embeddings import get_embeddings

_FALLBACK_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    separators=["\n\n", "\n", ". ", " ", ""],
)

_MAX_CHUNK_CHARS = 2000  # ~500 tokens at 4 chars/token; larger chunks fall back to recursive splitter


def chunk_document(pages: list[tuple[str, int]]) -> list[Document]:
    chunker = SemanticChunker(
        get_embeddings(),
        breakpoint_threshold_type="percentile",
    )

    all_chunks: list[Document] = []

    for page_text, page_num in pages:
        if not page_text.strip():
            continue

        raw_chunks = chunker.create_documents([page_text])

        page_chunks: list[Document] = []
        for chunk in raw_chunks:
            if len(chunk.page_content) > _MAX_CHUNK_CHARS:
                fallback = _FALLBACK_SPLITTER.split_documents(
                    [Document(page_content=chunk.page_content)]
                )
                page_chunks.extend(fallback)
            else:
                page_chunks.append(chunk)

        for chunk in page_chunks:
            chunk.metadata["page_number"] = page_num

        all_chunks.extend(page_chunks)

    for i, chunk in enumerate(all_chunks):
        chunk.metadata["chunk_index"] = i

    return all_chunks
