"""Embedding and vector store management using ChromaDB."""

from typing import List, Dict, Any
import chromadb


class EmbeddingStore:
    """Manages embeddings and vector store operations."""

    def __init__(self, persist_dir: str = "./chroma_db"):
        """Initialize embedding store with ChromaDB.

        Args:
            persist_dir: Directory to persist ChromaDB
        """
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = None

    def create_collection(self, name: str = "documents"):
        """Create or get a collection.

        Args:
            name: Name of the collection

        Returns:
            ChromaDB collection
        """
        self.collection = self.client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )
        return self.collection

    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the vector store.

        Args:
            documents: List of document chunks with metadata
        """
        if not self.collection:
            self.create_collection()

        ids = [str(doc["id"]) for doc in documents]
        documents_text = [doc["content"] for doc in documents]
        metadatas = [
            {
                "doc_id": str(doc["doc_id"]),
                "title": doc["title"],
                "category": doc["category"],
                "chunk_idx": str(doc["chunk_idx"]),
            }
            for doc in documents
        ]

        self.collection.add(
            ids=ids,
            documents=documents_text,
            metadatas=metadatas,
        )

    def similarity_search(
        self, query: str, k: int = 3
    ) -> tuple[List[Dict[str, Any]], List[float]]:
        """Search for similar documents.

        Args:
            query: Query text
            k: Number of results to return

        Returns:
            Tuple of (documents, distances)
        """
        if not self.collection:
            return [], []

        results = self.collection.query(
            query_texts=[query],
            n_results=k,
        )

        documents = []
        distances = []

        if results["documents"] and results["documents"][0]:
            for i, doc_text in enumerate(results["documents"][0]):
                doc_data = {
                    "content": doc_text,
                    "metadata": results["metadatas"][0][i],
                }
                documents.append(doc_data)
                distances.append(results["distances"][0][i])

        return documents, distances

    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get all documents from the collection.

        Returns:
            List of all documents
        """
        if not self.collection:
            return []

        results = self.collection.get()
        documents = []

        if results["documents"]:
            for i, doc_text in enumerate(results["documents"]):
                doc_data = {
                    "content": doc_text,
                    "metadata": results["metadatas"][i],
                }
                documents.append(doc_data)

        return documents

    def clear(self):
        """Clear the collection."""
        if self.collection:
            self.client.delete_collection(name=self.collection.name)
            self.collection = None
