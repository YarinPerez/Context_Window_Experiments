#!/usr/bin/env python3
"""
Execute Experiment 2 by querying the multi-document-extractor agent
for each test configuration.

NOTE: This script provides a framework and manual execution mode.
For full automation, integrate with Anthropic Claude API or Claude Code agent system.
"""

import json
import time
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Configuration
METADATA_FILE = Path("../inputs/metadata.json")
COMBINED_DIR = Path("../inputs/combined")
OUTPUT_FILE = Path("../outputs/extraction_results.json")

# Try to import tiktoken for accurate token counting
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    print("Warning: tiktoken not available. Using approximate token counting.")


def count_tokens(text: str) -> int:
    """
    Count tokens in text.

    Uses tiktoken if available, otherwise approximates as word_count * 1.3
    """
    if TIKTOKEN_AVAILABLE:
        try:
            # Use cl100k_base encoding (used by Claude models)
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except Exception as e:
            print(f"Warning: tiktoken error: {e}. Falling back to approximation.")

    # Fallback: approximate token count
    word_count = len(text.split())
    return int(word_count * 1.3)


def parse_json_response(response_text: str) -> Optional[Dict[str, Any]]:
    """
    Parse JSON from agent response, handling various formats.

    Args:
        response_text: Raw response text from agent

    Returns:
        Parsed JSON dict, or None if parsing fails
    """
    # Try direct JSON parse first
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    # Try to extract JSON from markdown code blocks
    json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    matches = re.findall(json_pattern, response_text, re.DOTALL)
    if matches:
        try:
            return json.loads(matches[0])
        except json.JSONDecodeError:
            pass

    # Try to find JSON object in text
    json_pattern = r'\{[^{}]*"answer"[^{}]*\}'
    matches = re.findall(json_pattern, response_text, re.DOTALL)
    if matches:
        try:
            return json.loads(matches[0])
        except json.JSONDecodeError:
            pass

    return None


def extract_answer_fallback(response_text: str) -> str:
    """
    Fallback method to extract answer if JSON parsing fails.

    Args:
        response_text: Raw response text

    Returns:
        Extracted answer or "PARSING_ERROR"
    """
    # Look for common answer patterns
    patterns = [
        r'"answer"\s*:\s*"([^"]+)"',
        r'answer:\s*"([^"]+)"',
        r'answer:\s*([0-9]{4})',  # Year pattern
        r'(?:the answer is|founded in)\s*([0-9]{4})',
    ]

    for pattern in patterns:
        match = re.search(pattern, response_text, re.IGNORECASE)
        if match:
            return match.group(1)

    return "PARSING_ERROR"


def invoke_agent_manual(combined_text: str, query: str) -> Dict[str, Any]:
    """
    Manual mode: Print instructions for user to execute query manually.

    This function will be called when automatic agent invocation is not available.
    It provides instructions for manual execution and prompts for results.

    Args:
        combined_text: The combined document text
        query: The query to ask

    Returns:
        Dict with answer, source_document_number, source_file, confidence
    """
    print("\n" + "=" * 70)
    print("MANUAL AGENT INVOCATION REQUIRED")
    print("=" * 70)
    print("\nPlease execute the following manually using Claude Code:")
    print("\n1. Ensure the multi-document-extractor agent is loaded")
    print(f"2. Provide the combined document (length: {len(combined_text)} chars)")
    print(f"3. Ask the query: \"{query}\"")
    print("\n4. The agent should return JSON like:")
    print('   {"answer": "1995", "source_document_number": 2, "source_file": "file_02_middle.txt", "confidence": "high"}')
    print("\n" + "=" * 70)

    # In a real implementation, this would call the Claude API or agent system
    # For now, return a placeholder structure
    print("\nWaiting for manual input...")
    print("(In production, this would be an API call)")

    # Simulate response (for testing purposes)
    # In real usage, replace this with actual agent invocation
    response = {
        "answer": "MANUAL_MODE_PLACEHOLDER",
        "source_document_number": 0,
        "source_file": "unknown",
        "confidence": "manual"
    }

    return response


def run_single_test(config: Dict[str, Any],
                   combined_dir: Path,
                   target_query: str,
                   target_answer: str,
                   manual_mode: bool = True) -> Dict[str, Any]:
    """
    Execute a single test configuration.

    Args:
        config: Test configuration from metadata
        combined_dir: Directory containing combined documents
        target_query: Query to ask
        target_answer: Expected answer
        manual_mode: If True, use manual invocation

    Returns:
        Result dictionary with all metrics
    """
    print(f"\n{'=' * 70}")
    print(f"Test: {config['test_id']} ({config['num_documents']} documents)")
    print(f"{'=' * 70}")

    # Load combined document
    combined_file = combined_dir / config["combined_file"]
    print(f"Loading: {combined_file}")

    with open(combined_file, 'r', encoding='utf-8') as f:
        combined_text = f.read()

    print(f"Document size: {len(combined_text):,} characters")

    # Count tokens
    print("Counting tokens...")
    input_tokens = count_tokens(combined_text)
    print(f"Input tokens: {input_tokens:,}")

    # Time the extraction
    print(f"Executing query: \"{target_query}\"")
    start_time = time.time()

    if manual_mode:
        result = invoke_agent_manual(combined_text, target_query)
    else:
        # In production, replace with actual API call
        # result = invoke_agent_api(combined_text, target_query)
        raise NotImplementedError("Automatic agent invocation not yet implemented")

    end_time = time.time()
    response_time_ms = int((end_time - start_time) * 1000)

    print(f"Response time: {response_time_ms}ms")

    # Extract answer
    extracted_answer = result.get("answer", "ERROR")
    print(f"Extracted answer: {extracted_answer}")

    # Count output tokens
    output_tokens = count_tokens(str(result))

    # Check correctness (flexible matching)
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
        "model": "claude-haiku-4.5",
        "source_document_number": result.get("source_document_number", 0),
        "source_file": result.get("source_file", "unknown"),
        "confidence": result.get("confidence", "unknown")
    }

    return result_entry


def main():
    """Run all experiment tests."""
    print("=" * 70)
    print("Experiment 2: Running Multi-Document Extraction Tests")
    print("=" * 70)
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

    # Check mode
    print("IMPORTANT: Manual mode is active.")
    print("For automatic execution, integrate with Claude API.")
    print()
    input("Press Enter to continue with manual mode, or Ctrl+C to abort...")

    results = []

    # Run each test
    for i, config in enumerate(configs, 1):
        print(f"\n\nTest {i}/{len(configs)}")

        try:
            result = run_single_test(
                config,
                COMBINED_DIR,
                target_query,
                target_answer,
                manual_mode=True
            )
            results.append(result)

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
                "model": "claude-haiku-4.5",
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
