# Experiment 2: Context Window Size Impact

## Executive Summary

This experiment tests the "Lost in the Middle" hypothesis in multi-document contexts. We investigate whether LLM retrieval accuracy degrades as the number of documents in the context window increases, particularly for information located in the middle of the document set.

## Research Question

**Primary Question**: Does information retrieval accuracy decline as the number of documents in a context window increases, especially for information in the middle of the document set?

**Secondary Questions**:
1. How does response time scale with the number of documents?
2. What is the relationship between token count and retrieval accuracy?
3. At what point (if any) does performance degradation become significant?

## Background

### Motivation

The "Lost in the Middle" phenomenon, documented in recent LLM research (Liu et al., 2023), suggests that language models struggle to access information in the middle of long contexts, exhibiting a U-shaped performance curve where items at the beginning and end are recalled better than those in the middle.

### Experiment 1 Context

Experiment 1 tested position effects *within* a single 6000-word document and found:
- **100% accuracy** across all positions (start, middle, end)
- No evidence of position-dependent retrieval degradation
- Claude Haiku 4.5 demonstrated position-independent performance

Experiment 2 extends this investigation to *multiple documents* in a single context.

## Hypothesis

### Primary Hypothesis

**H1**: Retrieval accuracy decreases as the number of documents in the context window increases, with the steepest decline occurring when the target document is positioned in the middle of a large document set.

**Expected Pattern**: Declining or U-shaped accuracy curve as document count increases from 2 to 50 documents.

### Null Hypothesis

**H0**: Document count does not significantly impact retrieval accuracy; Claude Haiku 4.5 maintains consistent performance regardless of context size or document position.

### Alternative Hypotheses

**H2**: Accuracy remains stable until a critical threshold (e.g., 20+ documents), after which degradation occurs.

**H3**: Response time increases super-linearly with document count, even if accuracy remains stable.

## Experimental Design

### Variables

**Independent Variable**: Number of documents in context (2, 5, 10, 20, 50)

**Dependent Variables**:
- Retrieval accuracy (binary: correct/incorrect)
- Response time (milliseconds)
- Token count (input + output)

**Controlled Variables**:
- Target query: "What year was the organization founded?"
- Target answer: "1995"
- Target document: file_02_middle.txt
- Target position: Always at the middle of the document set
- Document length: All documents ~6000 words
- Model: Claude Haiku 4.5

### Test Configurations

| Configuration | Total Docs | Middle Position | Target Index | Est. Tokens |
|--------------|-----------|-----------------|--------------|-------------|
| test_02_docs | 2         | 1               | 1            | ~16,000     |
| test_05_docs | 5         | 2               | 2            | ~40,000     |
| test_10_docs | 10        | 5               | 5            | ~80,000     |
| test_20_docs | 20        | 10              | 10           | ~160,000    |
| test_50_docs | 50        | 25              | 25           | ~400,000    |

### Document Selection Strategy

**Source Files**: 9 documents from Experiment 1 (file_01_end.txt through file_09_end.txt)

**Selection Algorithm**:
1. Identify middle position: `middle_pos = total_docs // 2`
2. Place target document (file_02_middle.txt) at middle position
3. Fill positions before middle by cycling through remaining 8 files
4. Fill positions after middle by continuing the cycle
5. Allow duplicates when document count exceeds 9

**Example (5 documents)**:
- Position 0: file_01_end.txt
- Position 1: file_03_end.txt
- Position 2: **file_02_middle.txt** (TARGET)
- Position 3: file_04_middle.txt
- Position 4: file_06_middle.txt

### Document Format

Documents are concatenated with clear separators:

```
====================================
DOCUMENT 1 OF 5
FILE: file_01_end.txt
====================================

[Full document content ~6000 words]

====================================
DOCUMENT 2 OF 5
FILE: file_03_end.txt
====================================

[Full document content ~6000 words]

...
```

## Methodology

### Phase 1: Document Generation

**Script**: `generate_combined_docs.py`

**Process**:
1. Load all 9 source documents from `../exp1/inputs/`
2. For each test configuration (2, 5, 10, 20, 50 docs):
   - Apply document selection algorithm
   - Concatenate documents with separators
   - Save to `inputs/combined/test_XX_docs.txt`
3. Generate `inputs/metadata.json` with test parameters

**Output**:
- 5 combined document files
- 1 metadata file with document orders and parameters

### Phase 2: Information Extraction

**Script**: `run_experiment.py`

**Process**:
1. Load each combined document
2. Start timer
3. Query Claude Haiku 4.5 via multi-document-extractor agent:
   - Input: Combined document + query
   - Expected: Extract "1995" from file_02_middle.txt
4. Stop timer
5. Record:
   - Extracted answer
   - Correctness (binary)
   - Response time
   - Token counts
   - Timestamp

**Agent**: `multi-document-extractor` (Claude Haiku 4.5)
- Parses multi-document context
- Searches all documents for answer
- Returns structured JSON with answer and source

**Output**: `outputs/extraction_results.json`

### Phase 3: Analysis

**Script**: `analyze_results.py`

**Metrics Computed**:

1. **Accuracy by Document Count**
   - Proportion of correct answers for each configuration
   - Overall accuracy across all tests

2. **Statistical Correlations**
   - Pearson correlation: document count vs accuracy
   - Pearson correlation: document count vs response time
   - Pearson correlation: token count vs accuracy

3. **Hypothesis Testing**
   - Determine if accuracy significantly degrades with doc count
   - Identify inflection points or thresholds
   - Compare to Experiment 1 baseline (100%)

**Output**:
- `outputs/analysis_results.json` (structured metrics)
- `outputs/final_report.md` (human-readable report)

### Phase 4: Visualization

**Script**: `visualize_results.py`

**Visualizations Created**:

1. **Accuracy vs Document Count** (line plot)
   - Shows retrieval accuracy decline (if any)
   - Includes Exp1 baseline at 100%

2. **Response Time vs Document Count** (scatter + trend line)
   - Demonstrates scaling behavior
   - Identifies linear/polynomial/exponential growth

3. **Token Count vs Document Count** (bar chart)
   - Visualizes context window growth
   - Separates input vs output tokens

4. **Combined Dashboard** (2x2 grid)
   - All metrics in single view
   - Summary statistics table

**Output**: 4 PNG files in `outputs/visualizations/`

## Expected Outcomes

### Scenario 1: Hypothesis Supported

**Pattern**:
- Accuracy: 100% → 95% → 85% → 70% → 60% (declining)
- Strong negative correlation (r < -0.7)
- Clear performance degradation at 20-50 docs

**Interpretation**:
- "Lost in the Middle" effect observed
- Claude Haiku struggles with large multi-document contexts
- Middle positioning amplifies retrieval difficulty

**Implications**:
- RAG systems should limit document count per query
- Document ranking/re-ranking becomes critical
- Consider chunking strategies for large document sets

### Scenario 2: Hypothesis Rejected

**Pattern**:
- Accuracy: 100% across all configurations
- Weak or no correlation (r > -0.3)
- Consistent performance regardless of doc count

**Interpretation**:
- No "Lost in the Middle" effect for multi-document contexts
- Claude Haiku maintains robust retrieval up to 50 docs
- Position-independent attention mechanisms effective

**Implications**:
- Larger document sets may be viable in RAG systems
- Context window size is the primary constraint, not document count
- Focus optimization efforts elsewhere (latency, cost)

### Scenario 3: Threshold Effect

**Pattern**:
- Accuracy: 100% → 100% → 95% → 70% → 50%
- Stable until ~10-20 docs, then sharp decline
- Inflection point identifies critical threshold

**Interpretation**:
- Performance stable within threshold
- Degradation occurs beyond critical capacity
- Claude Haiku has defined "sweet spot" for multi-doc retrieval

**Implications**:
- Optimal RAG systems should stay below threshold
- Design for ~5-10 documents per query
- Beyond threshold, use alternative strategies

## Evaluation Metrics

### Primary Metrics

1. **Accuracy**: Proportion of correct retrievals (0.0 to 1.0)
2. **Response Time**: Latency in milliseconds
3. **Token Count**: Total input + output tokens

### Secondary Metrics

1. **Correlation Coefficients**: Pearson r for key relationships
2. **Performance Degradation**: Change in accuracy from 2 to 50 docs
3. **Scaling Factor**: Growth rate of response time vs doc count

### Success Criteria

Experiment considered successful if:
- [ ] All 5 configurations execute without errors
- [ ] Complete data collected for all dependent variables
- [ ] Statistical analysis yields interpretable results
- [ ] Visualizations clearly communicate findings
- [ ] Hypothesis status (supported/rejected) is determinable

## Comparison to Experiment 1

| Aspect | Experiment 1 | Experiment 2 |
|--------|-------------|--------------|
| **Tested Variable** | Position within document | Number of documents |
| **Position Types** | Start, Middle, End | Always middle document |
| **Document Count** | 1 per test | 2, 5, 10, 20, 50 |
| **Context Size** | 6,000 words | 12K - 300K words |
| **Key Finding** | 100% accuracy (position-independent) | TBD |
| **Hypothesis** | U-shaped curve | Declining accuracy |
| **Result** | Hypothesis rejected | TBD |

## Limitations

1. **Single Query Type**: Only tests one query-answer pair
   - Future: Test multiple queries with varying complexity

2. **Single Model**: Only tests Claude Haiku 4.5
   - Future: Compare Haiku, Sonnet, Opus

3. **Fixed Document Length**: All docs ~6000 words
   - Future: Test with varying document lengths

4. **Deterministic Document Order**: Cycling pattern may create artifacts
   - Future: Randomize document order

5. **Single Position**: Target always at middle
   - Future: Test varied positions (start, middle, end)

6. **Homogeneous Content**: All documents have similar business-themed content
   - Future: Test with diverse content types

## Future Experiments

Based on Experiment 2 results, potential follow-up studies:

### Experiment 3: Position Variation
- Test target document at start, middle, end positions
- Confirm "Lost in the Middle" U-shaped curve

### Experiment 4: Model Comparison
- Compare Haiku, Sonnet, Opus performance
- Assess if larger models overcome retrieval challenges

### Experiment 5: Query Complexity
- Simple vs complex queries
- Single-fact vs multi-fact retrieval

### Experiment 6: Document Diversity
- Semantically similar vs dissimilar documents
- Test if similarity affects retrieval difficulty

### Experiment 7: Chunking Strategies
- Compare document-level vs chunk-level retrieval
- Assess optimal chunk size for large corpora

## References

1. Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2023). Lost in the Middle: How Language Models Use Long Contexts. *arXiv preprint arXiv:2307.03172*.

2. Anthropic. (2024). Claude Haiku 4.5 Technical Documentation.

3. Context Window Experiments - Experiment 1: Position-Based Retrieval Testing (2025).

## Appendices

### Appendix A: Document Statistics

All source documents (file_01_end.txt through file_09_end.txt):
- Word count: ~6000 words each
- Character count: ~35,000 characters each
- Estimated tokens: ~8,000 tokens each (using 1.3x word count)

### Appendix B: Hardware & Software

**Execution Environment**:
- OS: Linux
- Python: 3.8+
- Libraries: matplotlib, seaborn, numpy, tiktoken
- Model: Claude Haiku 4.5 via Anthropic API

### Appendix C: Data Availability

All experiment artifacts available in repository:
- Source documents: `exp1/inputs/`
- Combined documents: `exp2/inputs/combined/`
- Raw results: `exp2/outputs/extraction_results.json`
- Analysis: `exp2/outputs/analysis_results.json`
- Visualizations: `exp2/outputs/visualizations/`
- Scripts: `exp2/scripts/`

---

**Document Version**: 1.0
**Last Updated**: 2025-12-04
**Authors**: Isaac (with Claude Code assistance)
**License**: MIT
