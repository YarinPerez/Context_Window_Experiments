"""Evaluation and metrics framework."""

from typing import List, Dict, Any
import json


class Evaluator:
    """Evaluates retrieval performance."""

    def __init__(self):
        """Initialize evaluator."""
        self.results = []

    def calculate_context_size(self, documents: List[Dict]) -> int:
        """Calculate total context size in characters.

        Args:
            documents: List of documents

        Returns:
            Total character count
        """
        total = 0
        for doc in documents:
            total += len(doc["content"])
        return total

    def calculate_relevance_score(
        self, query: str, documents: List[Dict], expected_category: str = None
    ) -> float:
        """Calculate relevance score based on document categories.

        Args:
            query: Query text
            documents: Retrieved documents
            expected_category: Expected category for the query

        Returns:
            Relevance score (0-1)
        """
        if not documents or not expected_category:
            return 0.5

        relevant_count = 0
        for doc in documents:
            metadata = doc.get("metadata", {})
            if metadata.get("category") == expected_category:
                relevant_count += 1

        return relevant_count / len(documents) if documents else 0.0

    def evaluate_result(
        self,
        query: str,
        full_result: Dict[str, Any],
        rag_result: Dict[str, Any],
        expected_category: str = None,
    ) -> Dict[str, Any]:
        """Evaluate a comparison result.

        Args:
            query: Query text
            full_result: Result from full context mode
            rag_result: Result from RAG mode
            expected_category: Expected category for evaluation

        Returns:
            Evaluation metrics
        """
        full_context = full_result["documents"]
        rag_context = rag_result["documents"]

        full_size = self.calculate_context_size(full_context)
        rag_size = self.calculate_context_size(rag_context)

        full_relevance = self.calculate_relevance_score(
            query, full_context, expected_category
        )
        rag_relevance = self.calculate_relevance_score(
            query, rag_context, expected_category
        )

        metrics = {
            "query": query,
            "expected_category": expected_category,
            "full_context": {
                "context_size": full_size,
                "retrieval_time": full_result["retrieval_time"],
                "doc_count": full_result["documents_count"],
                "relevance_score": full_relevance,
            },
            "rag": {
                "context_size": rag_size,
                "retrieval_time": rag_result["retrieval_time"],
                "doc_count": rag_result["documents_count"],
                "relevance_score": rag_relevance,
            },
            "comparison": {
                "size_reduction": (1 - rag_size / full_size) * 100 if full_size > 0 else 0,
                "time_difference": full_result["retrieval_time"] - rag_result["retrieval_time"],
                "relevance_gain": rag_relevance - full_relevance,
            },
        }

        self.results.append(metrics)
        return metrics

    def aggregate_results(self) -> Dict[str, Any]:
        """Aggregate all evaluation results.

        Returns:
            Aggregated metrics
        """
        if not self.results:
            return {}

        avg_full_time = sum(r["full_context"]["retrieval_time"] for r in self.results) / len(self.results)
        avg_rag_time = sum(r["rag"]["retrieval_time"] for r in self.results) / len(self.results)
        avg_full_relevance = sum(r["full_context"]["relevance_score"] for r in self.results) / len(self.results)
        avg_rag_relevance = sum(r["rag"]["relevance_score"] for r in self.results) / len(self.results)
        avg_size_reduction = sum(r["comparison"]["size_reduction"] for r in self.results) / len(self.results)

        return {
            "total_queries": len(self.results),
            "full_context_avg_time": avg_full_time,
            "rag_avg_time": avg_rag_time,
            "full_context_avg_relevance": avg_full_relevance,
            "rag_avg_relevance": avg_rag_relevance,
            "avg_context_size_reduction": avg_size_reduction,
        }

    def save_results(self, filepath: str):
        """Save evaluation results to JSON.

        Args:
            filepath: Path to save results
        """
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
