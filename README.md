# LLM Context Window Experiments

A comprehensive research project investigating how Large Language Models (LLMs) retrieve and process information based on position, scale, and retrieval strategy within their context windows.

## Overview

These experiments systematically test the "lost in the middle" phenomenon and evaluate optimal strategies for information retrieval in LLM applications. The research progresses from single-document position testing to multi-document scaling, culminating in a practical comparison of RAG (Retrieval-Augmented Generation) versus full context approaches.

## Research Questions

1. **Position Effects**: Does information placement within a document affect retrieval accuracy?
2. **Scale Effects**: How does retrieval accuracy change as document count increases?
3. **Retrieval Strategy**: Is RAG more effective than providing full context?

## Experiments

### [Experiment 1: Position-Based Data Retrieval](exp1/)

**Goal**: Determine if LLMs retrieve data differently based on position within a **single document**.

**Hypothesis**: Information in the middle of a document will be retrieved less accurately than information at the start or end.

**Method**:
- 9 test files (~6,000 words each)
- 3 position categories: Start, Middle, End
- Extracted specific data points from each position

**Result**: ✅ **COMPLETED** | ❌ **HYPOTHESIS REJECTED**
- **Accuracy**: 100% across all positions
- **Finding**: No position effect observed within single documents
- **Model**: Claude Haiku 4.5

**Key Takeaway**: Information placement within typical documents (~6K words) does not affect retrieval accuracy.

---

### [Experiment 2: Context Window Size Impact](exp2/)

**Goal**: Test if retrieval accuracy decreases as the number of **documents** in the context increases.

**Hypothesis**: Retrieval accuracy degrades with increasing document count, especially for middle-positioned documents.

**Method**:
- 5 test configurations: 2, 5, 10, 20, 50 documents
- Target information always in middle document
- Each document ~6,000 words

**Result**: ✅ **COMPLETED** | ✅ **HYPOTHESIS SUPPORTED**
- **Overall Accuracy**: 80%
- **Finding**: 100% accuracy up to 20 documents, 0% at 50 documents
- **Correlation**: -0.936 (document count vs accuracy)
- **Model**: Claude Haiku 4.5

**Key Takeaway**: "Lost in the middle" effect emerges in multi-document contexts beyond 20 documents.

---

### [Experiment 3: RAG vs Full Context Comparison](exp3/)

**Goal**: Compare RAG with semantic search against providing full document context.

**Hypothesis**: RAG provides better relevance and efficiency than full context retrieval.

**Method**:
- 20 Hebrew documents across 3 domains (medicine, law, technology)
- 85 semantic chunks with vector embeddings
- 5 test queries comparing both approaches

**Result**: ✅ **COMPLETED** | ✅ **HYPOTHESIS SUPPORTED**
- **Context Reduction**: 85.5%
- **Relevance Improvement**: 96.7%
- **RAG Accuracy**: 67% relevance vs 34% full context
- **Vector Store**: ChromaDB with Nomic Embed Text

**Key Takeaway**: RAG dramatically improves efficiency and relevance for large document collections.

---

## Key Findings Summary

| Experiment | Accuracy | Finding | Implication |
|------------|----------|---------|-------------|
| **Exp 1: Single Document** | 100% | No position effect | Flexible content placement |
| **Exp 2: Multi-Document** | 80% | Critical threshold at 20-50 docs | Limit context to 10-20 docs |
| **Exp 3: RAG vs Full** | 67% vs 34% | RAG provides 96.7% relevance gain | Use RAG for large collections |

## Overall Conclusions

### 1. Position Effects Are Context-Dependent

**Within Single Documents**: No "lost in the middle" effect for typical document lengths (~6K words)
- Information can be placed anywhere without accuracy loss
- Modern LLMs handle single documents effectively

**Between Multiple Documents**: Strong "lost in the middle" effect emerges at scale
- Performance degrades beyond 20 documents
- Complete failure observed at 50 documents
- Position between documents matters significantly

**Conclusion**: Position effects manifest at the **document-set level**, not the **content level**.

### 2. Scale Is the Critical Factor

The number of documents in the context window is more impactful than position within a single document:

- ✅ **Safe Zone**: 1-10 documents (100% accuracy)
- ⚠️ **Warning Zone**: 10-20 documents (100% accuracy, approaching limit)
- ❌ **Danger Zone**: 20-50 documents (degradation begins)
- 🚫 **Failure Zone**: 50+ documents (0% accuracy observed)

### 3. RAG Is Essential for Large-Scale Retrieval

For document collections exceeding 20 documents, RAG is not optional—it's necessary:

**Without RAG (Full Context)**:
- 0% accuracy at 50 documents
- Massive context overhead (~390K tokens)
- Poor relevance (34% category match)
- Inefficient resource usage

**With RAG (Semantic Search)**:
- 85.5% context size reduction
- 96.7% relevance improvement
- 67% category match accuracy
- Efficient, focused retrieval

### 4. Model Performance

**Claude Haiku 4.5** demonstrated:
- Excellent single-document retrieval (100% accuracy)
- Strong performance up to 20 documents (100% accuracy)
- Failure at 50-document threshold (0% accuracy)
- Superior position-independent capabilities within documents

### 5. Practical Recommendations

#### For Single Documents
- ✅ **Place information naturally** - position doesn't matter
- ✅ **Focus on clarity** - semantic content > positional strategy
- ✅ **Optimize for readability** - no need for artificial positioning

#### For Multi-Document Applications
- ✅ **Limit to 5-10 documents** for optimal performance
- ✅ **Use 20 documents maximum** without RAG
- ❌ **Avoid 50+ documents** in raw context
- ✅ **Implement RAG** for larger collections

#### For RAG Systems
- ✅ **Always use semantic search** for 20+ documents
- ✅ **Prioritize document ranking** quality over quantity
- ✅ **Monitor context window usage** to stay below thresholds
- ✅ **Implement re-ranking** for critical applications
- ✅ **Use k=3-5 documents** for optimal balance

#### For Prompt Engineering
- ✅ **Single doc**: Position-agnostic prompts
- ✅ **Multi-doc**: Limit document count or use RAG
- ✅ **Large collections**: RAG is mandatory, not optional
- ✅ **Critical information**: Redundancy > positioning

## Repository Structure

```
Context_Window_Experiments/
├── exp1/                           # Experiment 1: Position-Based Retrieval
│   ├── docs/
│   │   └── context_window_experiment.md
│   ├── inputs/                     # 9 test files
│   ├── outputs/
│   │   └── phase_3_analysis.md
│   └── README.md
│
├── exp2/                           # Experiment 2: Multi-Document Scaling
│   ├── docs/
│   │   ├── experiment_2_design.md
│   │   └── README.md
│   ├── inputs/
│   │   ├── combined/               # Multi-document test files
│   │   └── metadata.json
│   ├── outputs/
│   │   ├── visualizations/         # Performance charts
│   │   ├── extraction_results.json
│   │   ├── analysis_results.json
│   │   └── final_report.md
│   ├── scripts/                    # Experiment automation
│   └── README.md
│
├── exp3/                           # Experiment 3: RAG vs Full Context
│   ├── src/                        # Python implementation
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   ├── retrieval.py
│   │   ├── evaluation.py
│   │   ├── analysis.py
│   │   └── run_experiment.py
│   ├── docs/
│   │   ├── EXPERIMENT.md
│   │   └── ANALYSIS.md
│   ├── data/
│   │   └── documents.json          # 20 Hebrew documents
│   ├── pyproject.toml
│   └── README.md
│
└── README.md                       # This file
```

## Quick Navigation

| Experiment | Description | Status | Hypothesis | Link |
|------------|-------------|--------|------------|------|
| **Experiment 1** | Position within single document | ✅ Complete | ❌ Rejected | [View Details](exp1/) |
| **Experiment 2** | Multi-document context scaling | ✅ Complete | ✅ Supported | [View Details](exp2/) |
| **Experiment 3** | RAG vs Full Context comparison | ✅ Complete | ✅ Supported | [View Details](exp3/) |

## Research Impact

### Theoretical Contributions

1. **Refined "Lost in the Middle" Understanding**: The phenomenon is real but context-dependent
2. **Threshold Identification**: Critical degradation occurs between 20-50 documents
3. **Position vs Scale**: Document count matters more than within-document position
4. **RAG Validation**: Empirical evidence for RAG necessity at scale

### Practical Applications

1. **RAG System Design**: Clear guidelines for document limits and retrieval strategies
2. **Prompt Engineering**: Evidence-based positioning recommendations
3. **Resource Optimization**: Context window usage efficiency
4. **Model Selection**: Performance characteristics for specific use cases

### Industry Relevance

- **Question Answering Systems**: Optimal document retrieval strategies
- **Document Processing**: Information extraction best practices
- **Chatbot Development**: Context management for conversational AI
- **Enterprise Search**: Large-scale document retrieval architecture

## Future Research Directions

### Potential Extensions

1. **Model Comparison**: Test across multiple LLM providers (GPT-4, Gemini, Claude variants)
2. **Threshold Refinement**: Test intermediate document counts (25, 30, 35, 40)
3. **Query Complexity**: Evaluate multi-step reasoning and complex inference tasks
4. **Domain Variation**: Test across different content types (code, legal, medical, technical)
5. **Multilingual Testing**: Extend beyond Hebrew to other languages
6. **Longer Documents**: Test 10K, 20K, 50K+ word documents for within-doc effects

### Open Questions

1. Are threshold effects consistent across different LLM architectures?
2. How do instruction-following and retrieval capabilities interact?
3. Can prompt engineering mitigate multi-document position effects?
4. What is the optimal k-value for RAG across different domains?
5. How do different embedding models affect RAG performance?

## Technical Details

### Models Tested
- **Claude Haiku 4.5**: All experiments (Anthropic)

### Evaluation Metrics
- Retrieval accuracy (exact match)
- Context window size (characters/tokens)
- Response time (milliseconds)
- Relevance score (category-based)
- Correlation analysis (Pearson)

### Technologies Used
- **Vector Store**: ChromaDB
- **Embeddings**: Nomic Embed Text (multilingual)
- **Languages**: Python, Hebrew (data)
- **Visualization**: Matplotlib
- **Analysis**: Statistical correlation, threshold detection

## Citation

If you use these experiments or findings in your research, please cite:

```bibtex
@research{context_window_experiments_2025,
  title={Comprehensive LLM Context Window Experiments: Position, Scale, and RAG Analysis},
  author={Isaac},
  year={2025},
  institution={Context Window Experiments},
  note={Three-part experimental study on LLM retrieval accuracy and context window effects}
}
```

## References

1. Liu, N. F., Lin, K., Hewitt, J., et al. (2023). "Lost in the Middle: How Language Models Use Long Contexts." *arXiv:2307.03172*
2. Anthropic. (2024). "Claude Haiku 4.5 Technical Documentation"
3. Lewis, P., et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *arXiv:2005.11401*
4. Segal, Yoram "Lab: Context Windows in Practice" (טנדוטס) כל הזכיות שמורות©

## License

MIT License - See repository for details

---

**Project Status**: All experiments completed (December 2025)
**Total Experiments**: 3
**Documents Tested**: 38 unique documents
**Queries Executed**: 14 test queries
**Key Finding**: Position effects are real but manifest at the document-set level, not within individual documents. RAG is essential for collections exceeding 20 documents.
