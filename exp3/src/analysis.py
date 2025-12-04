"""Analysis and visualization module."""

import json
from pathlib import Path
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import numpy as np


class ResultsAnalyzer:
    """Analyzes experiment results and generates visualizations."""

    def __init__(self, results_file: str = "results.json"):
        """Initialize analyzer.

        Args:
            results_file: Path to results JSON file
        """
        self.results = []
        self.aggregate = {}

        if Path(results_file).exists():
            with open(results_file, "r", encoding="utf-8") as f:
                self.results = json.load(f)

    def load_aggregate(self, aggregate_data: Dict[str, Any]):
        """Load aggregate metrics.

        Args:
            aggregate_data: Aggregate metrics dictionary
        """
        self.aggregate = aggregate_data

    def create_comparison_chart(self, output_path: str = "charts/comparison.png"):
        """Create context size and relevance comparison chart.

        Args:
            output_path: Output file path
        """
        if not self.results:
            return

        Path(output_path).parent.mkdir(exist_ok=True)

        queries = [r["query"][:30] for r in self.results]
        full_sizes = [r["full_context"]["context_size"] for r in self.results]
        rag_sizes = [r["rag"]["context_size"] for r in self.results]

        x = np.arange(len(queries))
        width = 0.35

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        ax1.bar(x - width / 2, full_sizes, width, label="Full Context", alpha=0.8)
        ax1.bar(x + width / 2, rag_sizes, width, label="RAG", alpha=0.8)
        ax1.set_xlabel("Query")
        ax1.set_ylabel("Context Size (chars)")
        ax1.set_title("Context Size Comparison")
        ax1.set_xticks(x)
        ax1.set_xticklabels(queries, rotation=45, ha="right")
        ax1.legend()

        full_relevance = [r["full_context"]["relevance_score"] for r in self.results]
        rag_relevance = [r["rag"]["relevance_score"] for r in self.results]

        ax2.bar(x - width / 2, full_relevance, width, label="Full Context", alpha=0.8)
        ax2.bar(x + width / 2, rag_relevance, width, label="RAG", alpha=0.8)
        ax2.set_xlabel("Query")
        ax2.set_ylabel("Relevance Score")
        ax2.set_title("Relevance Score Comparison")
        ax2.set_xticks(x)
        ax2.set_xticklabels(queries, rotation=45, ha="right")
        ax2.legend()
        ax2.set_ylim([0, 1])

        plt.tight_layout()
        plt.savefig(output_path, dpi=100, bbox_inches="tight")
        plt.close()

        print(f"Chart saved to {output_path}")

    def create_performance_chart(self, output_path: str = "charts/performance.png"):
        """Create retrieval time comparison chart with annotations.

        Args:
            output_path: Output file path
        """
        if not self.results:
            return

        Path(output_path).parent.mkdir(exist_ok=True)

        queries = [r["query"][:30] for r in self.results]
        rag_times = [r["rag"]["retrieval_time"] * 1000 for r in self.results]

        x = np.arange(len(queries))
        fig, ax = plt.subplots(figsize=(12, 6))

        bars = ax.bar(x, rag_times, width=0.6, label="RAG", alpha=0.8, color='#FF8C00')

        # Add value labels on bars
        for i, (bar, time) in enumerate(zip(bars, rag_times)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{time:.1f}ms', ha='center', va='bottom', fontweight='bold')

        # Add Full Context reference line at 0ms with annotation
        ax.axhline(y=0, color='green', linestyle='--', linewidth=2,
                  label='Full Context (0ms)', alpha=0.7)
        ax.text(-0.5, 5, 'Full Context: 0ms', fontsize=11, color='green',
               fontweight='bold', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))

        ax.set_xlabel("Query", fontsize=11, fontweight='bold')
        ax.set_ylabel("Retrieval Time (ms)", fontsize=11, fontweight='bold')
        ax.set_title("Retrieval Time: RAG vs Full Context\n(Note: Full Context is instantaneous at 0ms)",
                    fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(queries, rotation=45, ha="right")
        ax.legend(fontsize=10, loc='upper right')
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim([0, max(rag_times) * 1.2])

        plt.tight_layout()
        plt.savefig(output_path, dpi=100, bbox_inches="tight")
        plt.close()

        print(f"Chart saved to {output_path}")

    def generate_summary(self) -> str:
        """Generate a text summary of results.

        Returns:
            Summary string
        """
        if not self.aggregate:
            return "No aggregate data available"

        summary = "Experiment Summary\n"
        summary += "=" * 50 + "\n\n"

        summary += f"Total queries: {self.aggregate.get('total_queries', 0)}\n"
        summary += f"Full Context avg relevance: {self.aggregate.get('full_context_avg_relevance', 0):.4f}\n"
        summary += f"RAG avg relevance: {self.aggregate.get('rag_avg_relevance', 0):.4f}\n"
        summary += f"Avg context size reduction: {self.aggregate.get('avg_context_size_reduction', 0):.2f}%\n"
        summary += f"Full Context avg time: {self.aggregate.get('full_context_avg_time', 0):.6f}s\n"
        summary += f"RAG avg time: {self.aggregate.get('rag_avg_time', 0):.6f}s\n"

        return summary
