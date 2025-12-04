"""Main experiment runner script."""

import json
from pathlib import Path
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from chunking import DocumentChunker
from embeddings import EmbeddingStore
from retrieval import FullContextMode, RAGMode, RetrievalComparison
from evaluation import Evaluator


def load_queries() -> list[dict]:
    """Load test queries."""
    return [
        {
            "query": "מה הן תופעות הלוואי של תרופה X?",
            "category": "medicine"
        },
        {
            "query": "מה הם זכויות הצרכן?",
            "category": "law"
        },
        {
            "query": "איך טכנולוגיית ענן מגנה על נתונים?",
            "category": "technology"
        },
        {
            "query": "איך מטפלים בסוכרת?",
            "category": "medicine"
        },
        {
            "query": "מה הם חוקי הגירושין בישראל?",
            "category": "law"
        },
    ]


def setup_experiment():
    """Initialize experiment components."""
    print("Loading and chunking documents...")
    chunker = DocumentChunker(chunk_size=500, overlap=50)
    chunked_docs = chunker.load_and_chunk("data/documents.json")
    print(f"Created {len(chunked_docs)} chunks")

    print("Creating vector store...")
    store = EmbeddingStore(persist_dir="./chroma_db")
    store.create_collection("documents")
    store.add_documents(chunked_docs)
    print("Vector store ready")

    all_documents = store.get_all_documents()

    full_mode = FullContextMode(all_documents)
    rag_mode = RAGMode(store, k=3)

    return RetrievalComparison(full_mode, rag_mode), all_documents


def run_experiment():
    """Run the complete experiment."""
    print("=" * 60)
    print("RAG vs Full Context Comparison Experiment")
    print("=" * 60)

    comparison, all_docs = setup_experiment()
    evaluator = Evaluator()
    queries = load_queries()

    print(f"\nRunning {len(queries)} test queries...\n")

    for idx, q_data in enumerate(queries, 1):
        query = q_data["query"]
        category = q_data["category"]

        print(f"Query {idx}: {query[:50]}...")

        result = comparison.compare(query)
        metrics = evaluator.evaluate_result(
            query,
            result["full_context"],
            result["rag"],
            expected_category=category
        )

        print(f"  Full Context: {metrics['full_context']['doc_count']} docs, "
              f"{metrics['full_context']['context_size']} chars, "
              f"{metrics['full_context']['relevance_score']:.2f} relevance")
        print(f"  RAG: {metrics['rag']['doc_count']} docs, "
              f"{metrics['rag']['context_size']} chars, "
              f"{metrics['rag']['relevance_score']:.2f} relevance")
        print(f"  Size reduction: {metrics['comparison']['size_reduction']:.1f}%\n")

    print("=" * 60)
    print("Aggregate Results")
    print("=" * 60)
    aggregate = evaluator.aggregate_results()

    for key, value in aggregate.items():
        if isinstance(value, float):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")

    evaluator.save_results("results.json")
    print("\nResults saved to results.json")


if __name__ == "__main__":
    try:
        run_experiment()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
