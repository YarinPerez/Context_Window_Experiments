# Experiment 3: RAG vs Full Context Comparison

## Overview

This experiment compares two document retrieval strategies to determine the optimal balance between context quality and system efficiency:

1. **Full Context Mode**: Uses all available documents in the context window
2. **RAG Mode**: Uses only relevant documents retrieved via semantic similarity search

## Objective

To measure and compare the effectiveness of Retrieval-Augmented Generation (RAG) versus providing full context, evaluating:
- **Accuracy**: Relevance of retrieved documents to the query
- **Efficiency**: Context window size and retrieval latency
- **Quality**: Ability to answer queries correctly with minimal noise

## Methodology

### Data
- **Documents**: 20 documents in Hebrew covering three domains:
  - Medicine (side effects, treatment, health conditions)
  - Law (contracts, consumer rights, employment, intellectual property)
  - Technology (cloud computing, AI, databases, cybersecurity)
- **Document Format**: Each document contains a title, category, and detailed content

### Experimental Setup

#### Step 1: Document Chunking
- Split documents into overlapping chunks (500 characters, 50-character overlap)
- Preserve document metadata (title, category, chunk index)
- Total chunks created: 85 chunks from 20 documents

#### Step 2: Vector Embeddings
- Convert each chunk to vector embeddings using Nomic Embed Text
- Store embeddings in ChromaDB with cosine similarity distance metric
- Enable semantic search across documents

#### Step 3: Test Queries
Five test queries covering all domains:
1. "מה הן תופעות הלוואי של תרופה X?" (medicine)
2. "מה הם זכויות הצרכן?" (law)
3. "איך טכנולוגיית ענן מגנה על נתונים?" (technology)
4. "איך מטפלים בסוכרת?" (medicine)
5. "מה הם חוקי הגירושין בישראל?" (law)

#### Step 4: Comparison
For each query:
- **Full Context**: Retrieve all 85 chunks, use as context
- **RAG**: Retrieve top 3 most similar chunks via semantic search

#### Step 5: Evaluation
Metrics collected for each query:
- Context size (total characters in retrieved documents)
- Retrieval time (seconds)
- Relevance score (percentage of documents matching expected category)
- Document count

## Expected Results

### RAG Mode Advantages
- **Faster Retrieval**: Reduced computation time (few docs vs. all docs)
- **Smaller Context**: Less information overhead, fewer irrelevant chunks
- **Higher Relevance**: Only semantically similar documents included
- **Reduced Noise**: Less competing information confuses the model

### Full Context Mode Disadvantages
- **Slower Retrieval**: Must process all documents
- **Larger Context**: All chunks included regardless of relevance
- **Lower Relevance**: Mix of relevant and irrelevant information
- **Information Overload**: Model must filter through noise

## Expected Outcomes

Based on the pseudocode specification:
- **Context Size Reduction**: RAG should reduce context by ~70-80%
- **Relevance Improvement**: RAG should achieve 80%+ category match vs. 40-50% for full context
- **Time Efficiency**: RAG should be significantly faster for large document sets
- **Accuracy Trade-off**: RAG provides comparable or better quality despite smaller context

## Project Structure

```
exp3/
├── src/                          # Source code (max 150 lines per file)
│   ├── chunking.py              # Document chunking logic
│   ├── embeddings.py            # Vector store and ChromaDB integration
│   ├── retrieval.py             # RAG and full context retrieval modes
│   ├── evaluation.py            # Metrics calculation
│   ├── analysis.py              # Result visualization
│   ├── run_experiment.py        # Main experiment orchestrator
│   └── __init__.py
├── docs/                         # Documentation
│   ├── EXPERIMENT.md            # This file
│   └── ANALYSIS.md              # Results and findings
├── data/
│   └── documents.json           # 20 Hebrew test documents
├── pyproject.toml               # UV project configuration
├── .python-version              # Python 3.11
└── results.json                 # Experiment output
```

## Running the Experiment

### Setup
```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to project directory
cd exp3

# Create virtual environment and install dependencies
uv sync
```

### Execute
```bash
# Activate environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run experiment
python src/run_experiment.py

# Analyze results
python -c "from src.analysis import ResultsAnalyzer; \
    analyzer = ResultsAnalyzer(); \
    print(analyzer.generate_summary())"
```

## Success Criteria

The experiment is successful if:
1. ✓ All 5 test queries execute without errors
2. ✓ RAG relevance score ≥ full context relevance score
3. ✓ Context size reduction ≥ 60% with RAG
4. ✓ Retrieval time ≤ 0.1 seconds for both modes
5. ✓ RAG maintains accuracy while improving efficiency

## Notes

- **Language**: All documents and queries are in Hebrew
- **Embedding Model**: Nomic Embed Text (multilingual, open-source)
- **Vector DB**: ChromaDB (lightweight, persistent)
- **Evaluation Metric**: Category-based relevance scoring

---
