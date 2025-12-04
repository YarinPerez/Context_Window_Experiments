"""Document chunking module for splitting documents into manageable chunks."""

import json
from pathlib import Path
from typing import List, Dict, Any


class DocumentChunker:
    """Splits documents into chunks with optional overlap."""

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        """Initialize chunker with specified parameters.

        Args:
            chunk_size: Number of characters per chunk
            overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks.

        Args:
            text: Text to chunk

        Returns:
            List of text chunks
        """
        chunks = []
        step = self.chunk_size - self.overlap

        for i in range(0, len(text), step):
            chunk = text[i : i + self.chunk_size]
            if chunk.strip():
                chunks.append(chunk)

        return chunks

    def chunk_documents(self, documents: List[Dict]) -> List[Dict[str, Any]]:
        """Chunk a list of documents.

        Args:
            documents: List of document dictionaries

        Returns:
            List of chunked documents with metadata
        """
        chunked = []
        chunk_id = 0

        for doc in documents:
            text = f"{doc['title']}. {doc['content']}"
            chunks = self.chunk_text(text)

            for chunk_idx, chunk in enumerate(chunks):
                chunked.append({
                    "id": chunk_id,
                    "doc_id": doc["id"],
                    "title": doc["title"],
                    "category": doc["category"],
                    "chunk_idx": chunk_idx,
                    "content": chunk,
                })
                chunk_id += 1

        return chunked

    def load_and_chunk(self, json_path: str) -> List[Dict[str, Any]]:
        """Load documents from JSON and chunk them.

        Args:
            json_path: Path to JSON file with documents

        Returns:
            List of chunked documents
        """
        with open(json_path, "r", encoding="utf-8") as f:
            documents = json.load(f)

        return self.chunk_documents(documents)
