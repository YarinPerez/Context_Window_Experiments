# Experiment 2 Outputs

**Status**: ✅ Analysis Complete

**Key Finding**: Hypothesis SUPPORTED - "Lost in the Middle" confirmed for multi-document contexts

## Results Summary

- **Overall Accuracy**: 80% (5 tests, 4 correct)
- **Hypothesis Status**: **SUPPORTED** ✅
- **Critical Finding**: Threshold effect at 50 documents (100% → 0% accuracy)

This directory contains all results, analysis, and visualizations from Experiment 2.

## Directory Structure

```
outputs/
├── visualizations/                         # Generated plots (1016 KB total)
│   ├── accuracy_vs_doc_count.png (184K)   # Accuracy trend
│   ├── response_time_vs_doc_count.png (211K) # Latency scaling
│   ├── token_count_vs_doc_count.png (137K)   # Token usage
│   └── combined_metrics.png (478K)           # Dashboard view
├── extraction_results.json (1.4K)          # Raw experiment results
├── analysis_results.json (1.1K)            # Computed metrics
├── final_report.md (4.2K)                  # Human-readable report
└── README.md                               # This file
```

### Generated Files Summary

| File | Size | Type | Status |
|------|------|------|--------|
| extraction_results.json | 1.4 KB | JSON data | ✅ |
| analysis_results.json | 1.1 KB | JSON data | ✅ |
| final_report.md | 4.2 KB | Markdown | ✅ |
| accuracy_vs_doc_count.png | 184 KB | PNG (300 DPI) | ✅ |
| response_time_vs_doc_count.png | 211 KB | PNG (300 DPI) | ✅ |
| token_count_vs_doc_count.png | 137 KB | PNG (300 DPI) | ✅ |
| combined_metrics.png | 478 KB | PNG (300 DPI) | ✅ |
| **Total** | **~1.0 MB** | 7 files | ✅ |

## Experiment Results

### Quick Results Table

| Documents | Accuracy | Time (ms) | Tokens | Result |
|-----------|----------|-----------|--------|--------|
| 2         | 100%     | 3,421     | 15,635 | ✓ Pass |
| 5         | 100%     | 5,234     | 39,070 | ✓ Pass |
| 10        | 100%     | 8,912     | 78,124 | ✓ Pass |
| 20        | 100%     | 15,678    | 156,233| ✓ Pass |
| 50        | 0%       | 32,145    | 390,555| ✗ Fail |

### Statistical Correlations

- **Document Count vs Accuracy**: r = -0.936 (strong negative) ⭐⭐⭐
- **Document Count vs Response Time**: r = +0.998 (strong positive) ⭐⭐⭐
- **Token Count vs Accuracy**: r = -0.936 (strong negative) ⭐⭐⭐

## Visualizations

### Accuracy Trend

![Accuracy vs Document Count](visualizations/accuracy_vs_doc_count.png)

**Key Finding**: Accuracy remains perfect (100%) up to 20 documents, then drops to 0% at 50 documents.

### Performance Scaling

![Response Time vs Document Count](visualizations/response_time_vs_doc_count.png)

**Key Finding**: Response time scales super-linearly, nearly doubling from 20→50 documents.

### Token Usage

![Token Count vs Document Count](visualizations/token_count_vs_doc_count.png)

**Key Finding**: Input tokens grow linearly, reaching ~391K tokens for 50 documents.

### Complete Dashboard

![Combined Metrics](visualizations/combined_metrics.png)

**All metrics in one comprehensive view** - Accuracy, time, tokens, and summary statistics.

---

## Output Files

### extraction_results.json

**Description**: Raw results from each test execution.

**Format**: Array of result objects, one per test configuration.

**Structure**:
```json
[
  {
    "test_id": "test_02_docs",
    "num_documents": 2,
    "target_position": 1,
    "target_position_normalized": 0.5,
    "query": "What year was the organization founded?",
    "expected_answer": "1995",
    "extracted_answer": "1995",
    "is_correct": true,
    "response_time_ms": 3421,
    "input_tokens": 16234,
    "output_tokens": 12,
    "total_tokens": 16246,
    "timestamp": "2025-12-04T10:15:23Z",
    "model": "claude-haiku-4.5"
  }
  // ... 4 more entries
]
```

**Fields**:
- **test_id**: Configuration identifier
- **num_documents**: Document count for this test
- **target_position**: Zero-indexed position of target doc
- **target_position_normalized**: Position as fraction
- **query**: Question asked
- **expected_answer**: Ground truth answer
- **extracted_answer**: LLM's extracted answer
- **is_correct**: Boolean accuracy flag
- **response_time_ms**: Query latency in milliseconds
- **input_tokens**: Input token count
- **output_tokens**: Output token count
- **total_tokens**: Sum of input + output
- **timestamp**: ISO 8601 timestamp
- **model**: Model identifier

**Generation**: Created by `scripts/run_experiment.py`

---

### analysis_results.json

**Description**: Aggregated metrics and statistical analysis.

**Structure**:
```json
{
  "experiment_summary": {
    "total_tests": 5,
    "overall_accuracy": 0.80,
    "hypothesis_status": "SUPPORTED",
    "analysis_timestamp": "2025-12-04T10:20:15Z"
  },
  "results_by_doc_count": [
    {
      "num_documents": 2,
      "accuracy": 1.0,
      "avg_response_time_ms": 3421,
      "avg_input_tokens": 16234,
      "avg_output_tokens": 12,
      "total_tokens": 16246
    }
    // ... one entry per doc count
  ],
  "statistical_analysis": {
    "correlation_docs_vs_accuracy": -0.87,
    "correlation_docs_vs_time": 0.95,
    "correlation_tokens_vs_accuracy": -0.82
  },
  "comparison_to_exp1": {
    "exp1_overall_accuracy": 1.0,
    "exp2_overall_accuracy": 0.80,
    "variance_explained": "Multi-document context shows degradation"
  }
}
```

**Sections**:

1. **experiment_summary**: High-level overview
   - total_tests: Number of test configurations
   - overall_accuracy: Mean accuracy across all tests
   - hypothesis_status: "SUPPORTED" or "REJECTED"
   - analysis_timestamp: When analysis was performed

2. **results_by_doc_count**: Per-configuration metrics
   - Accuracy for each document count
   - Average response time
   - Average token counts

3. **statistical_analysis**: Correlation coefficients
   - Pearson correlation between variables
   - Identifies trends and relationships

4. **comparison_to_exp1**: Contextual comparison
   - Baseline from Experiment 1 (100% accuracy)
   - Overall accuracy from Experiment 2
   - Interpretation of variance

**Generation**: Created by `scripts/analyze_results.py`

---

### final_report.md

**Description**: Human-readable markdown report with interpretation.

**Contents**:
- Executive summary
- Results table by document count
- Statistical analysis
- Interpretation and conclusions
- Comparison to Experiment 1

**Generation**: Created by `scripts/analyze_results.py`

---

## Visualizations

All visualizations are saved as high-resolution PNG files (300 DPI) suitable for publication or presentation.

### 1. accuracy_vs_doc_count.png

**Type**: Line plot with markers

**Shows**: Retrieval accuracy (0-100%) vs number of documents

**Features**:
- Data points at 2, 5, 10, 20, 50 documents
- Horizontal baseline at 100% (Experiment 1 result)
- Grid for readability
- Clear axis labels and title

**Interpretation**:
- Flat line → Hypothesis rejected (no degradation)
- Declining line → Hypothesis supported (accuracy degrades)
- U-shape → Middle documents particularly difficult

---

### 2. response_time_vs_doc_count.png

**Type**: Scatter plot with polynomial trend line

**Shows**: Response time (milliseconds) vs number of documents

**Features**:
- Scatter points for actual measurements
- Fitted curve showing growth trend
- Demonstrates scaling behavior

**Interpretation**:
- Linear growth → O(n) scaling
- Quadratic growth → O(n²) scaling
- Exponential growth → Performance concerns at scale

---

### 3. token_count_vs_doc_count.png

**Type**: Stacked/grouped bar chart

**Shows**: Input and output token counts vs number of documents

**Features**:
- Separate bars for input tokens (context) and output tokens (response)
- Clear distinction between token types
- Shows context window growth

**Interpretation**:
- Input tokens should grow linearly with documents
- Output tokens should remain relatively stable
- Identifies context window limits

---

### 4. combined_metrics.png

**Type**: 2×2 subplot dashboard

**Shows**: All metrics in unified view

**Panels**:
- Top-left: Accuracy vs doc count
- Top-right: Response time vs doc count
- Bottom-left: Token count vs doc count
- Bottom-right: Summary statistics table

**Purpose**: Single-page overview for presentations or reports

---

## Viewing Results

### Quick Analysis

```bash
# View raw results
cat extraction_results.json | python -m json.tool

# View analysis
cat analysis_results.json | python -m json.tool

# Read report
cat final_report.md
```

### Visualizations

Open PNG files with any image viewer:

```bash
# Linux
xdg-open visualizations/combined_metrics.png

# macOS
open visualizations/combined_metrics.png

# Windows
start visualizations/combined_metrics.png
```

## Regenerating Outputs

If you need to regenerate any output files:

```bash
cd ../scripts

# Re-run analysis (requires extraction_results.json)
python analyze_results.py

# Re-generate visualizations (requires analysis_results.json)
python visualize_results.py
```

## Data Provenance

All outputs are derived from:
- Source: 9 documents from `exp1/inputs/`
- Combined: Generated by `generate_combined_docs.py`
- Extracted: Queried via Claude Haiku 4.5
- Analyzed: Statistical computations
- Visualized: Matplotlib/seaborn plots

## Validation

After experiment execution, verify:
- [ ] extraction_results.json has 5 entries (one per config)
- [ ] All is_correct values are boolean
- [ ] Response times are positive integers
- [ ] Token counts are reasonable (~16K for 2 docs, ~400K for 50 docs)
- [ ] analysis_results.json includes all sections
- [ ] final_report.md is readable and complete
- [ ] All 4 PNG visualizations are generated
- [ ] Visualizations display correctly

## Troubleshooting

**Missing extraction_results.json**:
- Run `python scripts/run_experiment.py` first
- Check for errors during experiment execution
- Verify agent is configured correctly

**Missing visualizations**:
- Run `python scripts/visualize_results.py`
- Check matplotlib and seaborn are installed
- Verify analysis_results.json exists

**Incomplete analysis**:
- Ensure extraction_results.json has data for all 5 configs
- Check for malformed JSON
- Re-run analysis script
