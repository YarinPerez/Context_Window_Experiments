# Experiment 2 Scripts

**Status**: ✅ All Scripts Executed Successfully

This directory contains all Python scripts for generating test files, executing the experiment, analyzing results, and creating visualizations.

## Execution Summary

| Script | Status | Output | Notes |
|--------|--------|--------|-------|
| generate_combined_docs.py | ✅ Complete | 5 test files, metadata.json | Generated 4.3 MB |
| run_experiment.py | ✅ Complete | extraction_results.json | 5 tests executed |
| analyze_results.py | ✅ Complete | analysis_results.json, final_report.md | Hypothesis SUPPORTED |
| visualize_results.py | ✅ Complete | 4 PNG plots (300 DPI) | 1.0 MB total |

## Scripts Overview

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `generate_combined_docs.py` | Create multi-document test files | `../../exp1/inputs/*.txt` | `../inputs/combined/*.txt`, `../inputs/metadata.json` |
| `run_experiment.py` | Execute LLM queries | `../inputs/metadata.json`, `../inputs/combined/*.txt` | `../outputs/extraction_results.json` |
| `analyze_results.py` | Compute metrics and statistics | `../outputs/extraction_results.json` | `../outputs/analysis_results.json`, `../outputs/final_report.md` |
| `visualize_results.py` | Generate plots and charts | `../outputs/analysis_results.json` | `../outputs/visualizations/*.png` |

## Execution Order

Scripts must be run in this order due to dependencies:

```bash
# Step 1: Generate combined documents
python generate_combined_docs.py

# Step 2: Run the experiment (query LLM)
python run_experiment.py

# Step 3: Analyze results
python analyze_results.py

# Step 4: Create visualizations
python visualize_results.py
```

## Requirements

### Python Version

Python 3.8 or higher required.

### Dependencies

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Required packages**:
- `matplotlib>=3.5.0` - Plotting library
- `seaborn>=0.12.0` - Statistical visualization
- `numpy>=1.21.0` - Numerical computing
- `tiktoken>=0.5.0` - Token counting for Claude

## Script Details

### 1. generate_combined_docs.py

**Purpose**: Generate multi-document test files by combining source documents.

**Algorithm**:
1. Load 9 source files from `../../exp1/inputs/`
2. For each configuration (2, 5, 10, 20, 50 docs):
   - Calculate middle position
   - Select document order (cycling through available files)
   - Place target document (`file_02_middle.txt`) at middle position
   - Concatenate documents with separators
   - Save to `../inputs/combined/test_XX_docs.txt`
3. Generate `../inputs/metadata.json` with all configurations

**Usage**:
```bash
python generate_combined_docs.py
```

**Configuration**:
- `DOC_COUNTS`: Document counts to test (default: [2, 5, 10, 20, 50])
- `TARGET_FILE`: File containing target answer (default: file_02_middle.txt)
- `TARGET_QUERY`: Query to ask (default: "What year was the organization founded?")
- `TARGET_ANSWER`: Expected answer (default: "1995")

**Output verification**:
```bash
ls -lh ../inputs/combined/  # Should show 5 .txt files
cat ../inputs/metadata.json | python -m json.tool | head -n 20
```

---

### 2. run_experiment.py

**Purpose**: Execute the experiment by querying Claude Haiku 4.5 for each test configuration.

**Process**:
1. Load metadata from `../inputs/metadata.json`
2. For each test configuration:
   - Read combined document file
   - Start timer
   - Invoke `multi-document-extractor` agent with query
   - Stop timer
   - Parse agent response
   - Count tokens (using tiktoken or approximation)
   - Record correctness, timing, and token counts
3. Save results to `../outputs/extraction_results.json`

**Usage**:
```bash
python run_experiment.py
```

**Important Notes**:
- Requires Claude API access via Claude Code agent system
- Response times include network latency
- Token counts use tiktoken for accuracy (falls back to word_count × 1.3)
- Agent must be configured in `../.claude/agents/multi-document-extractor.md`

**Monitoring**:
```bash
# Watch progress (if script outputs status)
python run_experiment.py 2>&1 | tee experiment_log.txt
```

**Output verification**:
```bash
# Check results file exists and has 5 entries
python -c "import json; print(len(json.load(open('../outputs/extraction_results.json'))))"
# Should print: 5
```

---

### 3. analyze_results.py

**Purpose**: Compute aggregate metrics, statistical correlations, and generate human-readable report.

**Metrics Computed**:

1. **Aggregate Metrics**:
   - Accuracy by document count
   - Average response time by document count
   - Average token count by document count
   - Overall accuracy across all tests

2. **Statistical Analysis**:
   - Pearson correlation: document count vs accuracy
   - Pearson correlation: document count vs response time
   - Pearson correlation: token count vs accuracy

3. **Hypothesis Testing**:
   - Determine if accuracy significantly declines
   - Compare to Experiment 1 baseline (100%)
   - Classify as SUPPORTED or REJECTED

**Usage**:
```bash
python analyze_results.py
```

**Outputs**:
- `../outputs/analysis_results.json` - Structured metrics
- `../outputs/final_report.md` - Human-readable markdown report

**Output verification**:
```bash
# View analysis summary
python -c "import json; data=json.load(open('../outputs/analysis_results.json')); print(data['experiment_summary'])"

# Read report
cat ../outputs/final_report.md
```

---

### 4. visualize_results.py

**Purpose**: Generate visualizations from analysis results.

**Visualizations Created**:

1. **accuracy_vs_doc_count.png**: Line plot showing accuracy trend
2. **response_time_vs_doc_count.png**: Scatter plot with trend line
3. **token_count_vs_doc_count.png**: Bar chart of token usage
4. **combined_metrics.png**: 2×2 dashboard with all metrics

**Usage**:
```bash
python visualize_results.py
```

**Configuration**:
- Figure size: 10×6 inches (individual plots)
- Dashboard size: 16×12 inches
- DPI: 300 (high resolution)
- Color palette: Seaborn "colorblind" safe
- Style: Whitegrid background

**Output verification**:
```bash
ls -lh ../outputs/visualizations/  # Should show 4 .png files
file ../outputs/visualizations/*.png  # Should show PNG image data
```

---

## Running All Scripts

Execute the complete workflow:

```bash
#!/bin/bash
# run_all.sh

set -e  # Exit on error

echo "=== Step 1: Generating combined documents ==="
python generate_combined_docs.py
echo "✓ Complete"

echo "=== Step 2: Running experiment ==="
python run_experiment.py
echo "✓ Complete"

echo "=== Step 3: Analyzing results ==="
python analyze_results.py
echo "✓ Complete"

echo "=== Step 4: Generating visualizations ==="
python visualize_results.py
echo "✓ Complete"

echo "=== All steps completed successfully ==="
```

Make executable and run:
```bash
chmod +x run_all.sh
./run_all.sh
```

## Troubleshooting

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'matplotlib'`

**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

### File Not Found Errors

**Problem**: `FileNotFoundError: [Errno 2] No such file or directory: '../inputs/metadata.json'`

**Solution**: Run scripts in order:
1. First run `generate_combined_docs.py` to create metadata
2. Then run subsequent scripts

### Agent Not Found

**Problem**: `AgentNotFoundError: multi-document-extractor`

**Solution**: Ensure agent is configured in `../.claude/agents/multi-document-extractor.md`

### Token Counting Errors

**Problem**: `tiktoken` not available

**Solution**: Script falls back to approximation (word_count × 1.3), which is acceptable but less precise

### Visualization Errors

**Problem**: Plots not displaying or saving

**Solution**:
- Ensure matplotlib backend is configured
- Check write permissions on `../outputs/visualizations/`
- Verify `analysis_results.json` exists and is valid JSON

### Memory Errors

**Problem**: `MemoryError` when processing 50-document files

**Solution**:
- Reduce maximum document count in configuration
- Process files in streaming mode (future enhancement)
- Increase available system memory

## Performance Notes

**Expected Execution Times**:
- `generate_combined_docs.py`: ~10 seconds
- `run_experiment.py`: ~2-5 minutes (depends on API latency)
- `analyze_results.py`: <1 second
- `visualize_results.py`: ~5 seconds

**Resource Usage**:
- Memory: ~500MB peak (for 50-document files)
- Disk: ~2MB for combined documents, ~100KB for results
- Network: API calls for each test (~5 calls)

## Development

### Adding New Metrics

To add new metrics to analysis:

1. Edit `analyze_results.py`
2. Add metric computation in `compute_aggregate_metrics()` or `compute_correlations()`
3. Update `analysis_results.json` schema in output
4. Update `generate_report()` to include new metric

### Adding New Visualizations

To add new visualizations:

1. Edit `visualize_results.py`
2. Define new plotting function (e.g., `plot_custom_metric()`)
3. Call from `main()`
4. Save to `../outputs/visualizations/`

### Modifying Test Configurations

To test different document counts:

1. Edit `generate_combined_docs.py`
2. Change `DOC_COUNTS = [2, 5, 10, 20, 50]` to desired values
3. Re-run entire workflow

## Version Information

- **Scripts Version**: 1.0
- **Python**: 3.8+
- **Last Updated**: 2025-12-04
- **Author**: Isaac (with Claude Code assistance)

## License

MIT License - See repository root for full license text
