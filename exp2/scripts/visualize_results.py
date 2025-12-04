#!/usr/bin/env python3
"""
Generate visualizations for Experiment 2 results.

Creates matplotlib/seaborn plots showing accuracy, response time,
token usage, and a combined dashboard.
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuration
ANALYSIS_FILE = Path("../outputs/analysis_results.json")
VIZ_DIR = Path("../outputs/visualizations")

# Visualization settings
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

# Set style
sns.set_style("whitegrid")
sns.set_palette("colorblind")


def load_analysis(analysis_file: Path):
    """Load analysis results from JSON file."""
    if not analysis_file.exists():
        raise FileNotFoundError(f"Analysis file not found: {analysis_file}")

    with open(analysis_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def plot_accuracy_vs_docs(data, output_file):
    """
    Plot accuracy vs document count.

    Args:
        data: List of results by document count
        output_file: Path to save plot
    """
    doc_counts = [d["num_documents"] for d in data]
    accuracies = [d["accuracy"] * 100 for d in data]

    plt.figure(figsize=(10, 6))

    # Plot data
    plt.plot(doc_counts, accuracies, marker='o', linewidth=2.5,
             markersize=10, color='#2E86AB', label='Experiment 2')

    # Add baseline from Experiment 1
    plt.axhline(y=100, color='#A23B72', linestyle='--', linewidth=2,
                label='Experiment 1 Baseline (100%)')

    # Formatting
    plt.xlabel('Number of Documents', fontsize=12, fontweight='bold')
    plt.ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
    plt.title('Retrieval Accuracy vs Document Count', fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)
    plt.legend(loc='best', framealpha=0.9)

    # Set y-axis range
    min_acc = min(accuracies) if accuracies else 0
    plt.ylim(max(0, min_acc - 10), 105)

    # Add value labels on points
    for x, y in zip(doc_counts, accuracies):
        plt.annotate(f'{y:.1f}%', (x, y), textcoords="offset points",
                    xytext=(0, 10), ha='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Created: {output_file.name}")


def plot_time_vs_docs(data, output_file):
    """
    Plot response time vs document count.

    Args:
        data: List of results by document count
        output_file: Path to save plot
    """
    doc_counts = np.array([d["num_documents"] for d in data])
    times = np.array([d["avg_response_time_ms"] for d in data])

    plt.figure(figsize=(10, 6))

    # Scatter plot
    plt.scatter(doc_counts, times, s=150, color='#F18F01',
               alpha=0.7, edgecolors='black', linewidth=1.5,
               label='Measured Time')

    # Fit trend line (polynomial degree 2)
    if len(doc_counts) >= 3:
        try:
            z = np.polyfit(doc_counts, times, 2)
            p = np.poly1d(z)
            x_smooth = np.linspace(doc_counts.min(), doc_counts.max(), 100)
            plt.plot(x_smooth, p(x_smooth), "r--", alpha=0.8,
                    linewidth=2, label='Trend (Polynomial Fit)')
        except:
            pass  # Skip trend line if fitting fails

    # Formatting
    plt.xlabel('Number of Documents', fontsize=12, fontweight='bold')
    plt.ylabel('Response Time (ms)', fontsize=12, fontweight='bold')
    plt.title('Response Time vs Document Count', fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)
    plt.legend(loc='best', framealpha=0.9)

    # Add value labels
    for x, y in zip(doc_counts, times):
        plt.annotate(f'{int(y)}ms', (x, y), textcoords="offset points",
                    xytext=(0, 10), ha='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Created: {output_file.name}")


def plot_tokens_vs_docs(data, output_file):
    """
    Plot token count vs document count.

    Args:
        data: List of results by document count
        output_file: Path to save plot
    """
    doc_counts = [d["num_documents"] for d in data]
    input_tokens = [d["avg_input_tokens"] for d in data]
    output_tokens = [d["avg_output_tokens"] for d in data]

    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(doc_counts))
    width = 0.35

    # Bar plots
    bars1 = ax.bar(x - width/2, input_tokens, width,
                   label='Input Tokens (Context)',
                   color='#06A77D', alpha=0.8, edgecolor='black', linewidth=1)

    bars2 = ax.bar(x + width/2, output_tokens, width,
                   label='Output Tokens (Response)',
                   color='#F72C25', alpha=0.8, edgecolor='black', linewidth=1)

    # Formatting
    ax.set_xlabel('Number of Documents', fontsize=12, fontweight='bold')
    ax.set_ylabel('Token Count', fontsize=12, fontweight='bold')
    ax.set_title('Token Usage vs Document Count', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(doc_counts)
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.8, axis='y')

    # Add value labels on bars (only for input tokens to avoid clutter)
    for i, (bar, val) in enumerate(zip(bars1, input_tokens)):
        height = bar.get_height()
        ax.annotate(f'{int(val/1000)}K',
                   xy=(bar.get_x() + bar.get_width() / 2, height),
                   xytext=(0, 3), textcoords="offset points",
                   ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Created: {output_file.name}")


def plot_combined_dashboard(data, analysis, output_file):
    """
    Create combined dashboard with all metrics.

    Args:
        data: List of results by document count
        analysis: Full analysis dictionary
        output_file: Path to save plot
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Experiment 2: Complete Analysis Dashboard',
                fontsize=20, fontweight='bold')

    doc_counts = [d["num_documents"] for d in data]

    # Top-left: Accuracy
    ax1 = axes[0, 0]
    accuracies = [d["accuracy"] * 100 for d in data]
    ax1.plot(doc_counts, accuracies, marker='o', linewidth=2.5,
            markersize=10, color='#2E86AB')
    ax1.axhline(y=100, color='#A23B72', linestyle='--', linewidth=2, alpha=0.7)
    ax1.set_xlabel('Documents')
    ax1.set_ylabel('Accuracy (%)')
    ax1.set_title('Accuracy vs Document Count', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(max(0, min(accuracies) - 10), 105)

    # Top-right: Response Time
    ax2 = axes[0, 1]
    times = [d["avg_response_time_ms"] for d in data]
    ax2.plot(doc_counts, times, marker='s', linewidth=2.5,
            markersize=10, color='#F18F01')
    ax2.set_xlabel('Documents')
    ax2.set_ylabel('Time (ms)')
    ax2.set_title('Response Time vs Document Count', fontweight='bold')
    ax2.grid(True, alpha=0.3)

    # Bottom-left: Tokens
    ax3 = axes[1, 0]
    tokens = [d["total_tokens"] for d in data]
    bars = ax3.bar(doc_counts, tokens, color='#06A77D', alpha=0.8,
                   edgecolor='black', linewidth=1)
    ax3.set_xlabel('Documents')
    ax3.set_ylabel('Total Tokens')
    ax3.set_title('Token Usage vs Document Count', fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')

    # Bottom-right: Summary table
    ax4 = axes[1, 1]
    ax4.axis('off')

    # Prepare table data
    table_data = []
    for d in data:
        table_data.append([
            str(d["num_documents"]),
            f"{d['accuracy']*100:.1f}%",
            f"{d['avg_response_time_ms']:.0f}",
            f"{d['total_tokens']:,}"
        ])

    # Add summary rows
    summary = analysis['experiment_summary']
    stats = analysis['statistical_analysis']

    table_data.append(['', '', '', ''])  # Separator
    table_data.append([
        'Overall',
        f"{summary['overall_accuracy']*100:.1f}%",
        '-',
        '-'
    ])
    table_data.append([
        'Hypothesis',
        summary['hypothesis_status'],
        '',
        ''
    ])
    table_data.append([
        'Corr (Doc/Acc)',
        f"{stats['correlation_docs_vs_accuracy']:.3f}",
        '',
        ''
    ])

    # Create table
    table = ax4.table(
        cellText=table_data,
        colLabels=['Docs', 'Accuracy', 'Time(ms)', 'Tokens'],
        loc='center',
        cellLoc='center',
        colWidths=[0.15, 0.2, 0.25, 0.25]
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.5)

    # Style header row
    for i in range(4):
        table[(0, i)].set_facecolor('#2E86AB')
        table[(0, i)].set_text_props(weight='bold', color='white')

    # Style summary rows
    for i in range(len(table_data) - 4, len(table_data)):
        for j in range(4):
            table[(i + 1, j)].set_facecolor('#F0F0F0')

    ax4.set_title('Summary Statistics', fontweight='bold', fontsize=12)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Created: {output_file.name}")


def main():
    """Generate all visualizations."""
    print("=" * 70)
    print("Experiment 2: Generating Visualizations")
    print("=" * 70)
    print()

    # Load analysis
    print(f"Loading analysis from: {ANALYSIS_FILE}")
    analysis = load_analysis(ANALYSIS_FILE)
    data = analysis["results_by_doc_count"]
    print(f"  Loaded data for {len(data)} document counts")
    print()

    # Create output directory
    VIZ_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {VIZ_DIR}")
    print()

    # Generate plots
    print("Generating visualizations...")

    plot_accuracy_vs_docs(data, VIZ_DIR / "accuracy_vs_doc_count.png")

    plot_time_vs_docs(data, VIZ_DIR / "response_time_vs_doc_count.png")

    plot_tokens_vs_docs(data, VIZ_DIR / "token_count_vs_doc_count.png")

    plot_combined_dashboard(data, analysis, VIZ_DIR / "combined_metrics.png")

    # Summary
    print("\n" + "=" * 70)
    print("Visualization Complete!")
    print("=" * 70)
    print(f"  Generated 4 plots in: {VIZ_DIR}")
    print(f"    - accuracy_vs_doc_count.png")
    print(f"    - response_time_vs_doc_count.png")
    print(f"    - token_count_vs_doc_count.png")
    print(f"    - combined_metrics.png")
    print()
    print("All files saved at 300 DPI for publication quality.")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
