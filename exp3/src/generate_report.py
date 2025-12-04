"""Generate analysis report and visualizations."""

import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from analysis import ResultsAnalyzer


def main():
    """Generate report with visualizations."""
    print("Loading results...")
    analyzer = ResultsAnalyzer("results.json")

    # Load aggregate metrics
    with open("results.json", "r", encoding="utf-8") as f:
        results = json.load(f)

    # Calculate aggregate
    full_times = [r["full_context"]["retrieval_time"] for r in results]
    rag_times = [r["rag"]["retrieval_time"] for r in results]
    full_relevance = [r["full_context"]["relevance_score"] for r in results]
    rag_relevance = [r["rag"]["relevance_score"] for r in results]
    size_reductions = [r["comparison"]["size_reduction"] for r in results]

    aggregate = {
        "total_queries": len(results),
        "full_context_avg_time": sum(full_times) / len(full_times),
        "rag_avg_time": sum(rag_times) / len(rag_times),
        "full_context_avg_relevance": sum(full_relevance) / len(full_relevance),
        "rag_avg_relevance": sum(rag_relevance) / len(rag_relevance),
        "avg_context_size_reduction": sum(size_reductions) / len(size_reductions),
    }

    analyzer.load_aggregate(aggregate)

    # Generate summary
    print("\n" + analyzer.generate_summary())

    # Create visualizations
    print("Creating visualizations...")
    Path("charts").mkdir(exist_ok=True)
    analyzer.create_comparison_chart("charts/comparison.png")
    analyzer.create_performance_chart("charts/performance.png")

    print("Report generation complete!")


if __name__ == "__main__":
    main()
