"""Retrieval strategies: RAG and full context modes."""

import time
from typing import List, Dict, Any
from embeddings import EmbeddingStore


class RetrievalMode:
    """Base class for retrieval modes."""

    def retrieve(self, query: str) -> tuple[List[Dict], float]:
        """Retrieve documents for a query.

        Args:
            query: Query text

        Returns:
            Tuple of (documents, retrieval_time)
        """
        raise NotImplementedError


class FullContextMode(RetrievalMode):
    """Retrieval mode using all documents."""

    def __init__(self, all_documents: List[Dict[str, Any]]):
        """Initialize with all documents.

        Args:
            all_documents: List of all document chunks
        """
        self.all_documents = all_documents

    def retrieve(self, query: str) -> tuple[List[Dict], float]:
        """Return all documents.

        Args:
            query: Query text (unused in full context mode)

        Returns:
            Tuple of (all_documents, retrieval_time)
        """
        start = time.time()
        context = [
            {
                "content": doc["content"],
                "metadata": doc["metadata"],
            }
            for doc in self.all_documents
        ]
        elapsed = time.time() - start
        return context, elapsed


class RAGMode(RetrievalMode):
    """Retrieval mode using similarity search (RAG)."""

    def __init__(self, store: EmbeddingStore, k: int = 3):
        """Initialize RAG mode.

        Args:
            store: EmbeddingStore instance
            k: Number of documents to retrieve
        """
        self.store = store
        self.k = k

    def retrieve(self, query: str) -> tuple[List[Dict], float]:
        """Retrieve similar documents for a query.

        Args:
            query: Query text

        Returns:
            Tuple of (relevant_documents, retrieval_time)
        """
        start = time.time()
        documents, _ = self.store.similarity_search(query, k=self.k)
        elapsed = time.time() - start
        return documents, elapsed


class RetrievalComparison:
    """Compare retrieval modes."""

    def __init__(
        self,
        full_mode: FullContextMode,
        rag_mode: RAGMode,
    ):
        """Initialize comparison.

        Args:
            full_mode: FullContextMode instance
            rag_mode: RAGMode instance
        """
        self.full_mode = full_mode
        self.rag_mode = rag_mode

    def compare(self, query: str) -> Dict[str, Any]:
        """Compare both retrieval modes for a query.

        Args:
            query: Query text

        Returns:
            Dictionary with results from both modes
        """
        full_docs, full_time = self.full_mode.retrieve(query)
        rag_docs, rag_time = self.rag_mode.retrieve(query)

        return {
            "query": query,
            "full_context": {
                "documents_count": len(full_docs),
                "retrieval_time": full_time,
                "documents": full_docs,
            },
            "rag": {
                "documents_count": len(rag_docs),
                "retrieval_time": rag_time,
                "documents": rag_docs,
            },
        }
