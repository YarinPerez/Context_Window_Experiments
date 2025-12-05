#!/usr/bin/env python3
"""
Generate combined multi-document test files for Experiment 2.

This script loads source documents from Experiment 1 and combines them into
multi-document test files with the target document always positioned at the
middle of each document set.
"""

import json
import itertools
from pathlib import Path
from typing import List, Dict

# Configuration
SOURCE_DIR = Path("../../exp1/inputs")
OUTPUT_DIR = Path("../inputs/combined")
METADATA_FILE = Path("../inputs/metadata.json")

TARGET_FILE = "file_02_middle.txt"
TARGET_QUERY = "What year was the organization founded?"
TARGET_ANSWER = "1995"

DOC_COUNTS = [20, 25, 30, 35, 40, 45, 50]

SEPARATOR_TEMPLATE = """====================================
DOCUMENT {num} OF {total}
FILE: {filename}
====================================

"""


def load_source_files(source_dir: Path) -> Dict[str, str]:
    """
    Load all source files into memory.

    Args:
        source_dir: Directory containing source .txt files

    Returns:
        Dictionary mapping filename to file content
    """
    files = {}
    txt_files = sorted(source_dir.glob("file_*.txt"))

    if not txt_files:
        raise FileNotFoundError(f"No source files found in {source_dir}")

    for txt_file in txt_files:
        with open(txt_file, 'r', encoding='utf-8') as f:
            files[txt_file.name] = f.read()

    print(f"Loaded {len(files)} source files from {source_dir}")
    return files


def select_document_order(num_docs: int, target_file: str,
                         available_files: List[str]) -> List[str]:
    """
    Deterministically select document order with target at middle position.

    Args:
        num_docs: Total number of documents needed
        target_file: Filename of target document (placed at middle)
        available_files: List of all available filenames

    Returns:
        List of filenames in order
    """
    middle_pos = num_docs // 2
    order = []

    # Create list of files excluding target
    other_files = [f for f in available_files if f != target_file]

    # Create infinite cycle through other files
    file_cycle = itertools.cycle(other_files)

    # Fill positions before middle
    for i in range(middle_pos):
        order.append(next(file_cycle))

    # Insert target at middle position
    order.append(target_file)

    # Fill positions after middle
    for i in range(middle_pos + 1, num_docs):
        order.append(next(file_cycle))

    return order


def create_combined_document(files: Dict[str, str],
                            order: List[str]) -> str:
    """
    Combine multiple documents with separators.

    Args:
        files: Dictionary mapping filenames to content
        order: List of filenames in desired order

    Returns:
        Combined document string
    """
    combined = []
    total = len(order)

    for i, filename in enumerate(order, 1):
        # Add separator header
        separator = SEPARATOR_TEMPLATE.format(
            num=i,
            total=total,
            filename=filename
        )
        combined.append(separator)

        # Add document content
        combined.append(files[filename])

        # Add blank line between documents
        combined.append("\n")

    return "".join(combined)


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def estimate_tokens(word_count: int) -> int:
    """Estimate token count from word count (using 1.3x multiplier)."""
    return int(word_count * 1.3)


def main():
    """Generate all combined test documents and metadata."""
    print("=" * 60)
    print("Experiment 2: Generating Combined Documents")
    print("=" * 60)
    print()

    # Load source files
    print("Step 1: Loading source documents...")
    source_files = load_source_files(SOURCE_DIR)
    available_files = sorted(source_files.keys())
    print(f"  Available files: {', '.join(available_files)}")
    print()

    # Verify target file exists
    if TARGET_FILE not in available_files:
        raise ValueError(f"Target file '{TARGET_FILE}' not found in source directory")

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate metadata structure
    metadata = {
        "experiment_name": "Context Window Size Impact",
        "experiment_version": "2.0",
        "target_query": TARGET_QUERY,
        "target_answer": TARGET_ANSWER,
        "target_file": TARGET_FILE,
        "model": "claude-haiku-4.5",
        "test_configurations": []
    }

    # Generate each test configuration
    print("Step 2: Generating combined documents...")
    for num_docs in DOC_COUNTS:
        test_id = f"test_{num_docs:02d}_docs"
        output_file = OUTPUT_DIR / f"{test_id}.txt"

        print(f"\n  Configuration: {num_docs} documents")

        # Select document order
        order = select_document_order(num_docs, TARGET_FILE, available_files)
        target_pos = order.index(TARGET_FILE)

        print(f"    Document order: {', '.join(order[:3])}{'...' if num_docs > 3 else ''}")
        print(f"    Target position: {target_pos} (zero-indexed)")

        # Create combined document
        combined = create_combined_document(source_files, order)

        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(combined)

        # Calculate statistics
        word_count = count_words(combined)
        estimated_tokens = estimate_tokens(word_count)

        print(f"    Word count: {word_count:,}")
        print(f"    Estimated tokens: {estimated_tokens:,}")
        print(f"    Saved to: {output_file.name}")

        # Add to metadata
        config = {
            "test_id": test_id,
            "num_documents": num_docs,
            "target_position": target_pos,
            "target_position_normalized": target_pos / (num_docs - 1) if num_docs > 1 else 0.5,
            "combined_file": output_file.name,
            "document_order": order,
            "total_word_count": word_count,
            "estimated_tokens": estimated_tokens
        }
        metadata["test_configurations"].append(config)

    # Save metadata
    print("\nStep 3: Saving metadata...")
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

    print(f"  Metadata saved to: {METADATA_FILE}")

    # Summary
    print("\n" + "=" * 60)
    print("Generation Complete!")
    print("=" * 60)
    print(f"  Generated files: {len(DOC_COUNTS)}")
    print(f"  Document counts tested: {', '.join(map(str, DOC_COUNTS))}")
    print(f"  Total output size: ~{sum(c['total_word_count'] for c in metadata['test_configurations']) / 1000:.0f}K words")
    print(f"  Metadata file: {METADATA_FILE}")
    print()
    print("Next step: Run run_experiment.py to execute the experiment")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
