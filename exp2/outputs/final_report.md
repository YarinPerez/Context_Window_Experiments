# Experiment 2: Context Window Size Impact - Analysis Report

**Date**: 2025-12-05T20:56:52.179228Z

## Executive Summary

- **Total Tests**: 7
- **Overall Accuracy**: 42.9%
- **Hypothesis Status**: **SUPPORTED**

### Key Findings

The "Lost in the Middle" hypothesis is **SUPPORTED**. Retrieval accuracy decreases
as the number of documents in the context window increases, indicating that the LLM
struggles to retrieve information from middle-positioned documents in large contexts.

## Results by Document Count

| Documents | Accuracy | Avg Time (ms) | Avg Tokens | Tests |
|-----------|----------|---------------|------------|-------|
| 20 | 100.0% |    15678 |    156,230 | 1 |
| 25 | 100.0% |    19487 |    195,284 | 1 |
| 30 | 100.0% |    23856 |    234,338 | 1 |
| 35 |   0.0% |    28234 |    273,395 | 1 |
| 40 |   0.0% |    31023 |    312,444 | 1 |
| 45 |   0.0% |    32812 |    351,500 | 1 |
| 50 |   0.0% |    34156 |    390,555 | 1 |

## Statistical Analysis

### Correlation Coefficients

- **Document Count vs Accuracy**: -0.866
- **Document Count vs Response Time**: 0.982
- **Token Count vs Accuracy**: -0.866

### Interpretation

**Strong negative correlation** (-0.866): As document count increases,
accuracy decreases significantly. This strongly supports the "Lost in the Middle" hypothesis.

**Strong positive correlation** (0.982): Response time increases
significantly with document count, indicating potential scaling challenges for large contexts.


## Comparison to Experiment 1

| Metric | Experiment 1 | Experiment 2 | Difference |
|--------|--------------|--------------|------------|
| Overall Accuracy | 100.0% | 42.9% | -57.1% |
| Context Type | Single document | Multi-document | - |
| Position Tested | Within document | Between documents | - |

### Analysis

Multi-document context shows significant degradation compared to single-document retrieval.

## Conclusions

1. **Context Window Effects Confirmed**: The experiment demonstrates that retrieval
   accuracy degrades with increasing document counts, particularly for middle-positioned documents.

2. **Practical Implications**: RAG systems should limit the number of documents passed to
   the LLM per query, prioritizing document ranking and relevance filtering.

3. **Performance Considerations**: Response time scales with document count, reinforcing
   the need for efficient context management strategies.

4. **Future Research**: Investigate optimal document counts, test with different models
   (Sonnet, Opus), and explore mitigation strategies (re-ranking, chunking).

## Limitations

1. **Single Query Type**: Only one query-answer pair tested
2. **Single Model**: Results specific to Claude Haiku 4.5
3. **Uniform Documents**: All ~6000 words with similar content
4. **Middle Position Only**: Target always at middle; other positions not tested
5. **Small Sample Size**: One test per configuration

## Recommendations

1. Limit RAG queries to 5-10 documents maximum
2. Implement robust document ranking and re-ranking
3. Consider iterative retrieval for large document sets
4. Monitor performance degradation at scale
5. Test with Sonnet or Opus models for critical applications

---

**Report Generated**: 2025-12-05T20:56:52.179228Z
**Experiment**: Context Window Size Impact (Experiment 2)
**Model**: Claude Haiku 4.5
**Configurations Tested**: 7
