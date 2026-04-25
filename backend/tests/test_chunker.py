from unittest.mock import patch, MagicMock
from langchain_core.documents import Document
from app.documents.chunker import chunk_document


def test_chunk_document_returns_documents():
    pages = [("This is a test sentence about vacation policy. Another sentence about PTO.", 1)]

    with patch("app.documents.chunker.SemanticChunker") as MockChunker:
        mock_instance = MagicMock()
        mock_instance.create_documents.return_value = [
            Document(page_content="This is a test sentence about vacation policy.")
        ]
        MockChunker.return_value = mock_instance

        chunks = chunk_document(pages)

    assert len(chunks) >= 1
    assert all(isinstance(c, Document) for c in chunks)


def test_chunk_document_adds_chunk_index():
    pages = [("Sentence one. Sentence two. Sentence three.", 1)]

    with patch("app.documents.chunker.SemanticChunker") as MockChunker:
        mock_instance = MagicMock()
        mock_instance.create_documents.return_value = [
            Document(page_content="Sentence one."),
            Document(page_content="Sentence two."),
        ]
        MockChunker.return_value = mock_instance

        chunks = chunk_document(pages)

    assert chunks[0].metadata["chunk_index"] == 0
    assert chunks[1].metadata["chunk_index"] == 1


def test_chunk_document_adds_page_number():
    pages = [("Page one content here.", 3)]

    with patch("app.documents.chunker.SemanticChunker") as MockChunker:
        mock_instance = MagicMock()
        mock_instance.create_documents.return_value = [
            Document(page_content="Page one content here.")
        ]
        MockChunker.return_value = mock_instance

        chunks = chunk_document(pages)

    assert chunks[0].metadata["page_number"] == 3


def test_chunk_document_skips_empty_pages():
    pages = [("", 1), ("   ", 2), ("Real content here.", 3)]

    with patch("app.documents.chunker.SemanticChunker") as MockChunker:
        mock_instance = MagicMock()
        mock_instance.create_documents.return_value = [
            Document(page_content="Real content here.")
        ]
        MockChunker.return_value = mock_instance

        chunks = chunk_document(pages)

    assert len(chunks) == 1
    assert MockChunker.return_value.create_documents.call_count == 1


def test_chunk_document_falls_back_for_oversized_chunks():
    long_text = "word " * 600  # ~3000 chars > 2000 token estimate
    pages = [(long_text, 1)]

    with patch("app.documents.chunker.SemanticChunker") as MockChunker:
        mock_instance = MagicMock()
        mock_instance.create_documents.return_value = [
            Document(page_content=long_text)
        ]
        MockChunker.return_value = mock_instance

        chunks = chunk_document(pages)

    # Fallback splits the long chunk into smaller ones
    assert all(len(c.page_content) <= 1200 for c in chunks)
