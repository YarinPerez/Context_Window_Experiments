#!/usr/bin/env python3
"""
Automated Experiment 2 runner using Anthropic API.

This script automatically runs all 7 test configurations by querying
Claude via the Anthropic API with each combined document.
"""

import json
import time
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Try to import anthropic
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("Error: anthropic package not installed.")
    print("Install with: pip install anthropic")
    exit(1)

# Configuration
METADATA_FILE = Path("../inputs/metadata.json")
COMBINED_DIR = Path("../inputs/combined")
OUTPUT_FILE = Path("../outputs/extraction_results.json")

# Model to use
MODEL = "claude-haiku-4-20250514"  # Claude Haiku 4.5


def extract_answer_from_response(response_text: str, target_answer: str) -> tuple[str, str, str]:
    """
    Extract answer, source document, and confidence from response.

    Returns:
        Tuple of (answer, source_file, confidence)
    """
    # Try to parse as JSON first
    try:
        import re
        # Look for JSON in the response
        json_match = re.search(r'\{[^{}]*"answer"[^{}]*\}', response_text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            return (
                data.get("answer", "UNKNOWN"),
                data.get("source_file", "unknown"),
                data.get("confidence", "unknown")
            )
    except:
        pass

    # Fallback: look for the year in the response
    import re
    year_match = re.search(r'\b(19\d{2}|20\d{2})\b', response_text)
    if year_match:
        return (year_match.group(1), "unknown", "medium")

    return ("EXTRACTION_FAILED", "unknown", "low")


def run_single_test(client: anthropic.Anthropic,
                   config: Dict[str, Any],
                   combined_dir: Path,
                   target_query: str,
                   target_answer: str) -> Dict[str, Any]:
    """
    Execute a single test configuration using Anthropic API.

    Args:
        client: Anthropic API client
        config: Test configuration from metadata
        combined_dir: Directory containing combined documents
        target_query: Query to ask
        target_answer: Expected answer

    Returns:
        Result dictionary with all metrics
    """
    print(f"\n{'=' * 70}")
    print(f"Test: {config['test_id']} ({config['num_documents']} documents)")
    print(f"{'=' * 70}")

    # Load combined document
    combined_file = combined_dir / config["combined_file"]
    print(f"Loading: {combined_file.name}")

    with open(combined_file, 'r', encoding='utf-8') as f:
        combined_text = f.read()

    print(f"Document size: {len(combined_text):,} characters")
    print(f"Estimated tokens: {config['estimated_tokens']:,}")

    # Prepare the prompt
    prompt = f"""You are analyzing a multi-document collection. Your task is to find and extract specific information.

{combined_text}

Question: {target_query}

Please provide your answer in the following JSON format:
{{
  "answer": "your answer here",
  "source_document_number": <document number where you found the answer>,
  "source_file": "filename where you found the answer",
  "confidence": "high|medium|low"
}}"""

    # Time the API call
    print(f"Executing query: \"{target_query}\"")
    print("Calling Anthropic API...")
    start_time = time.time()

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        end_time = time.time()
        response_time_ms = int((end_time - start_time) * 1000)

        # Extract response text
        response_text = response.content[0].text

        # Get token usage
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

        print(f"Response time: {response_time_ms}ms")
        print(f"Input tokens: {input_tokens:,}")
        print(f"Output tokens: {output_tokens:,}")

        # Extract answer
        extracted_answer, source_file, confidence = extract_answer_from_response(
            response_text, target_answer
        )

        print(f"Extracted answer: {extracted_answer}")

        # Check correctness
        is_correct = (
            extracted_answer.strip().lower() == target_answer.strip().lower() or
            target_answer.strip().lower() in extracted_answer.strip().lower()
        )
        print(f"Correctness: {'✓ CORRECT' if is_correct else '✗ INCORRECT'}")

        # Build result entry
        result_entry = {
            "test_id": config["test_id"],
            "num_documents": config["num_documents"],
            "target_position": config["target_position"],
            "target_position_normalized": config["target_position_normalized"],
            "query": target_query,
            "expected_answer": target_answer,
            "extracted_answer": extracted_answer,
            "is_correct": is_correct,
            "response_time_ms": response_time_ms,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "model": MODEL,
            "source_file": source_file,
            "confidence": confidence,
            "raw_response": response_text[:500]  # Store first 500 chars for debugging
        }

        return result_entry

    except Exception as e:
        end_time = time.time()
        response_time_ms = int((end_time - start_time) * 1000)

        print(f"ERROR: {e}")

        return {
            "test_id": config["test_id"],
            "num_documents": config["num_documents"],
            "target_position": config["target_position"],
            "target_position_normalized": config["target_position_normalized"],
            "query": target_query,
            "expected_answer": target_answer,
            "extracted_answer": "API_ERROR",
            "is_correct": False,
            "response_time_ms": response_time_ms,
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "model": MODEL,
            "error": str(e)
        }


def main():
    """Run all experiment tests automatically."""
    print("=" * 70)
    print("Experiment 2: Automated Multi-Document Extraction Tests")
    print("=" * 70)
    print()

    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
        print()
        print("Please set your API key:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        print()
        print("Or run with:")
        print("  ANTHROPIC_API_KEY='your-key' python3 run_experiment_auto.py")
        exit(1)

    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key=api_key)
    print("✓ Anthropic API client initialized")
    print(f"✓ Using model: {MODEL}")
    print()

    # Check if metadata exists
    if not METADATA_FILE.exists():
        print(f"Error: Metadata file not found: {METADATA_FILE}")
        print("Please run generate_combined_docs.py first.")
        return

    # Load metadata
    print(f"Loading metadata from: {METADATA_FILE}")
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    target_query = metadata["target_query"]
    target_answer = metadata["target_answer"]
    configs = metadata["test_configurations"]

    print(f"Target query: \"{target_query}\"")
    print(f"Expected answer: \"{target_answer}\"")
    print(f"Test configurations: {len(configs)}")
    print()

    print("Starting automated experiment...")
    print("This will take approximately 3-5 minutes.")
    print()

    results = []

    # Run each test
    for i, config in enumerate(configs, 1):
        print(f"\n\nTest {i}/{len(configs)}")

        try:
            result = run_single_test(
                client,
                config,
                COMBINED_DIR,
                target_query,
                target_answer
            )
            results.append(result)

            # Small delay between requests to avoid rate limiting
            if i < len(configs):
                time.sleep(1)

        except KeyboardInterrupt:
            print("\n\nExperiment interrupted by user.")
            break
        except Exception as e:
            print(f"\nError in test {config['test_id']}: {e}")
            import traceback
            traceback.print_exc()

            # Add error entry
            results.append({
                "test_id": config["test_id"],
                "num_documents": config["num_documents"],
                "target_position": config["target_position"],
                "target_position_normalized": config["target_position_normalized"],
                "query": target_query,
                "expected_answer": target_answer,
                "extracted_answer": "ERROR",
                "is_correct": False,
                "response_time_ms": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "model": MODEL,
                "error": str(e)
            })

    # Save results
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n\nSaving results to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    # Summary
    print("\n" + "=" * 70)
    print("Experiment Complete!")
    print("=" * 70)
    print(f"  Total tests: {len(results)}")
    correct = sum(1 for r in results if r.get("is_correct", False))
    print(f"  Correct answers: {correct}/{len(results)} ({correct/len(results)*100:.1f}%)")
    print(f"  Results saved to: {OUTPUT_FILE}")
    print()
    print("Next step: Run analyze_results.py to analyze the data")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExperiment aborted by user.")
        exit(1)
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
