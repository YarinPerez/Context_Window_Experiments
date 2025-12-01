# LLM Context Window Position Experiment

## Experiment Overview

This experiment investigates how effectively Large Language Models (LLMs) retrieve specific data points based on their position within the context window.

## Purpose

To evaluate the accuracy of LLM data retrieval as a function of information placement within the context window, specifically testing whether retrieval performance varies when target data appears at different positions (beginning, middle, or end).

## Background

LLMs process input text within a finite context window. Research suggests that retrieval accuracy may be influenced by the position of relevant information within this window—a phenomenon sometimes referred to as the "lost in the middle" effect.

## Hypothesis

**Primary Hypothesis:** LLMs will demonstrate high accuracy in retrieving data located at the beginning or end of the context window, but will show reduced accuracy for data positioned in the middle of the context window.

**Expected Pattern:**
- **High accuracy**: Data at start of context
- **Low accuracy**: Data in middle of context  
- **High accuracy**: Data at end of context

## Experimental Design

### Materials

**Test Files:** 9 text files with substantial word counts designed to fill the LLM's context window

**Key Data Points:** Each file will contain a specific piece of target information (e.g., "The CEO of the company is David Cohen")

### File Organization

The 9 files will be distributed across three position categories:

| Position Category | Number of Files | Data Location |
|------------------|-----------------|---------------|
| **Start Position** | 3 files | Key data appears at the beginning |
| **Middle Position** | 3 files | Key data appears in the middle |
| **End Position** | 3 files | Key data appears at the end |

### Variables

**Independent Variable:** Position of target data within the context window (start, middle, end)

**Dependent Variable:** Accuracy of data retrieval by the LLM

**Control Variables:**
- File length (word count)
- Type of target information
- Complexity of surrounding text
- LLM model and version

## Methodology

### Phase 1: File Generation
1. Generate 9 text files with large word counts
2. Embed unique key data points in each file
3. Position data according to experimental design (3 files per position)
4. Ensure files are of sufficient length to fill the context window

### Phase 2: Testing
1. Present each file to the LLM individually
2. Query the LLM to retrieve the specific key data point
3. Record the accuracy of each retrieval attempt
4. Document any partial or incorrect retrievals

### Phase 3: Analysis
1. Calculate retrieval accuracy for each position category
2. Compare accuracy rates across start, middle, and end positions
3. Analyze statistical significance of observed differences
4. Identify any patterns or anomalies in the results

## Expected Outcomes

Based on the hypothesis, we anticipate:

- **Start position files:** ≥80% retrieval accuracy
- **Middle position files:** ≤60% retrieval accuracy
- **End position files:** ≥80% retrieval accuracy

## Potential Applications

Understanding how LLMs handle positional information in their context window can inform:
- Prompt engineering best practices
- Document structuring for LLM processing
- Information retrieval system design
- RAG (Retrieval-Augmented Generation) architecture optimization

## Notes

- The specific key data point may vary between files to ensure independence of trials
- Results may vary depending on the specific LLM model, version, and context window size
- Future iterations could test additional variables such as data complexity or semantic similarity of surrounding text
