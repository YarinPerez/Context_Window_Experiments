#!/usr/bin/env python3
"""
Analyze Experiment 2 results and generate statistical summaries.

Computes aggregate metrics, correlation coefficients, and generates
both machine-readable JSON and human-readable markdown reports.
"""

import json
import statistics
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Configuration
RESULTS_FILE = Path("../outputs/extraction_results.json")
ANALYSIS_FILE = Path("../outputs/analysis_results.json")
REPORT_FILE = Path("../outputs/final_report.md")


def load_results(results_file: Path) -> List[Dict[str, Any]]:
    """
    Load extraction results from JSON file.

    Args:
        results_file: Path to extraction_results.json

    Returns:
        List of result dictionaries
    """
    if not results_file.exists():
        raise FileNotFoundError(f"Results file not found: {results_file}")

    with open(results_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def compute_aggregate_metrics(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Compute aggregate metrics by document count.

    Args:
        results: List of individual test results

    Returns:
        List of aggregated metrics per document count
    """
    # Group by document count
    by_doc_count = {}

    for result in results:
        num_docs = result["num_documents"]
        if num_docs not in by_doc_count:
            by_doc_count[num_docs] = []
        by_doc_count[num_docs].append(result)

    # Compute aggregates
    aggregated = []

    for num_docs in sorted(by_doc_count.keys()):
        tests = by_doc_count[num_docs]

        # Calculate metrics
        accuracy = sum(t.get("is_correct", False) for t in tests) / len(tests)

        # Only calculate averages if we have valid data
        valid_times = [t["response_time_ms"] for t in tests if t.get("response_time_ms", 0) > 0]
        avg_time = statistics.mean(valid_times) if valid_times else 0

        valid_input_tokens = [t["input_tokens"] for t in tests if t.get("input_tokens", 0) > 0]
        avg_input_tokens = statistics.mean(valid_input_tokens) if valid_input_tokens else 0

        valid_output_tokens = [t["output_tokens"] for t in tests if t.get("output_tokens", 0) > 0]
        avg_output_tokens = statistics.mean(valid_output_tokens) if valid_output_tokens else 0

        aggregated.append({
            "num_documents": num_docs,
            "accuracy": accuracy,
            "avg_response_time_ms": round(avg_time, 2),
            "avg_input_tokens": int(avg_input_tokens),
            "avg_output_tokens": int(avg_output_tokens),
            "total_tokens": int(avg_input_tokens + avg_output_tokens),
            "num_tests": len(tests)
        })

    return aggregated


def pearson_correlation(x: List[float], y: List[float]) -> float:
    """
    Compute Pearson correlation coefficient.

    Args:
        x: First variable
        y: Second variable

    Returns:
        Correlation coefficient (-1 to 1)
    """
    if len(x) != len(y) or len(x) < 2:
        return 0.0

    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi ** 2 for xi in x)
    sum_y2 = sum(yi ** 2 for yi in y)

    numerator = n * sum_xy - sum_x * sum_y
    denominator = ((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2)) ** 0.5

    if denominator == 0:
        return 0.0

    return numerator / denominator


def compute_correlations(aggregated: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Compute correlation coefficients between variables.

    Args:
        aggregated: Aggregated metrics by document count

    Returns:
        Dictionary of correlation coefficients
    """
    doc_counts = [a["num_documents"] for a in aggregated]
    accuracies = [a["accuracy"] for a in aggregated]
    times = [a["avg_response_time_ms"] for a in aggregated]
    tokens = [a["total_tokens"] for a in aggregated]

    return {
        "correlation_docs_vs_accuracy": round(pearson_correlation(doc_counts, accuracies), 3),
        "correlation_docs_vs_time": round(pearson_correlation(doc_counts, times), 3),
        "correlation_tokens_vs_accuracy": round(pearson_correlation(tokens, accuracies), 3)
    }


def determine_hypothesis_status(correlation_docs_vs_accuracy: float,
                                overall_accuracy: float) -> str:
    """
    Determine if hypothesis is supported or rejected.

    Args:
        correlation_docs_vs_accuracy: Correlation coefficient
        overall_accuracy: Overall accuracy rate

    Returns:
        "SUPPORTED" or "REJECTED"
    """
    # Hypothesis is supported if:
    # 1. Strong negative correlation (< -0.5), OR
    # 2. Overall accuracy significantly lower than Exp1 (< 0.90)

    if correlation_docs_vs_accuracy < -0.5:
        return "SUPPORTED"
    elif overall_accuracy < 0.90:
        return "SUPPORTED"
    else:
        return "REJECTED"


def generate_report(analysis: Dict[str, Any], output_file: Path):
    """
    Generate human-readable markdown report.

    Args:
        analysis: Analysis results dictionary
        output_file: Path to save report
    """
    summary = analysis['experiment_summary']
    by_doc = analysis['results_by_doc_count']
    stats = analysis['statistical_analysis']
    comparison = analysis['comparison_to_exp1']

    report = f"""# Experiment 2: Context Window Size Impact - Analysis Report

**Date**: {summary['analysis_timestamp']}

## Executive Summary

- **Total Tests**: {summary['total_tests']}
- **Overall Accuracy**: {summary['overall_accuracy'] * 100:.1f}%
- **Hypothesis Status**: **{summary['hypothesis_status']}**

### Key Findings

"""

    # Add key findings based on hypothesis status
    if summary['hypothesis_status'] == "SUPPORTED":
        report += """The "Lost in the Middle" hypothesis is **SUPPORTED**. Retrieval accuracy decreases
as the number of documents in the context window increases, indicating that the LLM
struggles to retrieve information from middle-positioned documents in large contexts.

"""
    else:
        report += """The "Lost in the Middle" hypothesis is **REJECTED**. Claude Haiku 4.5 maintains
consistent retrieval accuracy regardless of document count, demonstrating robust
position-independent information retrieval capabilities.

"""

    # Results table
    report += """## Results by Document Count

| Documents | Accuracy | Avg Time (ms) | Avg Tokens | Tests |
|-----------|----------|---------------|------------|-------|
"""

    for result in by_doc:
        report += f"| {result['num_documents']:2d} | {result['accuracy']*100:5.1f}% | {result['avg_response_time_ms']:8.0f} | {result['total_tokens']:10,} | {result['num_tests']} |\n"

    # Statistical analysis
    report += f"""
## Statistical Analysis

### Correlation Coefficients

- **Document Count vs Accuracy**: {stats['correlation_docs_vs_accuracy']:.3f}
- **Document Count vs Response Time**: {stats['correlation_docs_vs_time']:.3f}
- **Token Count vs Accuracy**: {stats['correlation_tokens_vs_accuracy']:.3f}

### Interpretation

"""

    # Interpret correlations
    corr_acc = stats['correlation_docs_vs_accuracy']
    if corr_acc < -0.7:
        report += f"""**Strong negative correlation** ({corr_acc:.3f}): As document count increases,
accuracy decreases significantly. This strongly supports the "Lost in the Middle" hypothesis.

"""
    elif corr_acc < -0.3:
        report += f"""**Moderate negative correlation** ({corr_acc:.3f}): There is some degradation
in accuracy with increased document count, providing partial support for the hypothesis.

"""
    else:
        report += f"""**Weak or no correlation** ({corr_acc:.3f}): Document count does not
significantly impact accuracy. The LLM maintains consistent performance across context sizes.

"""

    corr_time = stats['correlation_docs_vs_time']
    if corr_time > 0.7:
        report += f"""**Strong positive correlation** ({corr_time:.3f}): Response time increases
significantly with document count, indicating potential scaling challenges for large contexts.

"""
    elif corr_time > 0.3:
        report += f"""**Moderate positive correlation** ({corr_time:.3f}): Response time shows
some increase with document count, but scaling appears manageable.

"""

    # Comparison to Experiment 1
    report += f"""
## Comparison to Experiment 1

| Metric | Experiment 1 | Experiment 2 | Difference |
|--------|--------------|--------------|------------|
| Overall Accuracy | {comparison['exp1_overall_accuracy']*100:.1f}% | {comparison['exp2_overall_accuracy']*100:.1f}% | {(comparison['exp2_overall_accuracy'] - comparison['exp1_overall_accuracy'])*100:+.1f}% |
| Context Type | Single document | Multi-document | - |
| Position Tested | Within document | Between documents | - |

### Analysis

{comparison['variance_explained']}

"""

    # Conclusions
    report += """## Conclusions

"""

    if summary['hypothesis_status'] == "SUPPORTED":
        report += """1. **Context Window Effects Confirmed**: The experiment demonstrates that retrieval
   accuracy degrades with increasing document counts, particularly for middle-positioned documents.

2. **Practical Implications**: RAG systems should limit the number of documents passed to
   the LLM per query, prioritizing document ranking and relevance filtering.

3. **Performance Considerations**: Response time scales with document count, reinforcing
   the need for efficient context management strategies.

4. **Future Research**: Investigate optimal document counts, test with different models
   (Sonnet, Opus), and explore mitigation strategies (re-ranking, chunking).

"""
    else:
        report += """1. **Robust Retrieval Capabilities**: Claude Haiku 4.5 demonstrates consistent
   accuracy regardless of document count, suggesting advanced position-independent attention mechanisms.

2. **Practical Implications**: RAG systems using Claude Haiku 4.5 can safely utilize larger
   document contexts without accuracy concerns, though token limits and latency remain considerations.

3. **Contrast with Published Research**: These results differ from the "Lost in the Middle"
   findings in Liu et al. (2023), possibly due to model improvements or experimental differences.

4. **Future Research**: Test with even larger document counts, compare across model families,
   and investigate the boundaries of this robust performance.

"""

    # Limitations
    report += """## Limitations

1. **Single Query Type**: Only one query-answer pair tested
2. **Single Model**: Results specific to Claude Haiku 4.5
3. **Uniform Documents**: All ~6000 words with similar content
4. **Middle Position Only**: Target always at middle; other positions not tested
5. **Small Sample Size**: One test per configuration

## Recommendations

"""

    if summary['hypothesis_status'] == "SUPPORTED":
        report += """1. Limit RAG queries to 5-10 documents maximum
2. Implement robust document ranking and re-ranking
3. Consider iterative retrieval for large document sets
4. Monitor performance degradation at scale
5. Test with Sonnet or Opus models for critical applications
"""
    else:
        report += """1. Leverage larger context windows with confidence
2. Focus optimization efforts on latency and cost
3. Continue monitoring for degradation at extreme scales (100+ docs)
4. Consider testing with more complex queries
5. Validate findings with diverse document types
"""

    report += f"""
---

**Report Generated**: {summary['analysis_timestamp']}
**Experiment**: Context Window Size Impact (Experiment 2)
**Model**: Claude Haiku 4.5
**Configurations Tested**: {summary['total_tests']}
"""

    # Write report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)


def main():
    """Analyze results and generate reports."""
    print("=" * 70)
    print("Experiment 2: Analyzing Results")
    print("=" * 70)
    print()

    # Load results
    print(f"Loading results from: {RESULTS_FILE}")
    results = load_results(RESULTS_FILE)
    print(f"  Loaded {len(results)} test results")
    print()

    # Compute metrics
    print("Computing aggregate metrics...")
    aggregated = compute_aggregate_metrics(results)
    print(f"  Aggregated data for {len(aggregated)} document counts")
    print()

    print("Computing correlations...")
    correlations = compute_correlations(aggregated)
    for key, value in correlations.items():
        print(f"  {key}: {value:.3f}")
    print()

    # Overall accuracy
    overall_accuracy = sum(r.get("is_correct", False) for r in results) / len(results) if results else 0
    print(f"Overall accuracy: {overall_accuracy * 100:.1f}%")

    # Determine hypothesis status
    hypothesis_status = determine_hypothesis_status(
        correlations["correlation_docs_vs_accuracy"],
        overall_accuracy
    )
    print(f"Hypothesis status: {hypothesis_status}")
    print()

    # Build analysis structure
    analysis = {
        "experiment_summary": {
            "total_tests": len(results),
            "overall_accuracy": round(overall_accuracy, 3),
            "hypothesis_status": hypothesis_status,
            "analysis_timestamp": datetime.utcnow().isoformat() + "Z"
        },
        "results_by_doc_count": aggregated,
        "statistical_analysis": correlations,
        "comparison_to_exp1": {
            "exp1_overall_accuracy": 1.0,
            "exp2_overall_accuracy": round(overall_accuracy, 3),
            "variance_explained": (
                "Multi-document context shows significant degradation compared to single-document retrieval."
                if overall_accuracy < 0.95
                else "Multi-document context maintains accuracy similar to single-document retrieval."
            )
        }
    }

    # Save analysis
    print(f"Saving analysis to: {ANALYSIS_FILE}")
    ANALYSIS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ANALYSIS_FILE, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2)

    # Generate report
    print(f"Generating report: {REPORT_FILE}")
    generate_report(analysis, REPORT_FILE)

    # Summary
    print("\n" + "=" * 70)
    print("Analysis Complete!")
    print("=" * 70)
    print(f"  Analysis file: {ANALYSIS_FILE}")
    print(f"  Report file: {REPORT_FILE}")
    print(f"  Overall accuracy: {overall_accuracy * 100:.1f}%")
    print(f"  Hypothesis: {hypothesis_status}")
    print()
    print("Next step: Run visualize_results.py to generate plots")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
