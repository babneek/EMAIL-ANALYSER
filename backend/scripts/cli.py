#!/usr/bin/env python3
"""
Sales Email Thread Analytics — CLI Application
Usage: python cli.py --input ../tests/data/sample_emails.json --output report.csv
"""

import argparse
import json
import sys
import os
from dotenv import load_dotenv

# Ensure the root 'backend' directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.analyzer import identify_threads, analyze_threads
from app.utils.csv_exporter import export_to_csv

# Load .env from backend directory
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

def main():
    parser = argparse.ArgumentParser(
        description="Analyze sales email conversations and generate a CSV analytics report."
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to the input JSON file containing email conversations"
    )
    parser.add_argument(
        "--output", "-o",
        default="email_thread_analytics.csv",
        help="Path for the output CSV file (default: email_thread_analytics.csv)"
    )
    parser.add_argument(
        "--model",
        default="llama-3.1-8b-instant",
        help="Model to use (default: llama-3.1-8b-instant)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed progress output"
    )

    args = parser.parse_args()

    # Check API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY not found. Set it in .env file or environment.")
        sys.exit(1)

    # Load input file
    print(f"Loading emails from: {args.input}")
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            emails_data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Input file not found: {args.input}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in input file: {e}")
        sys.exit(1)

    # Step 1: Identification (Simplified as the new analyze_threads handles it)
    print("Step 1/2: Analyzing threads (sentiment, risk, requirements)...")
    analysis = analyze_threads(json.dumps(emails_data), api_key, args.model, args.verbose)
    if not analysis:
        print("ERROR: Failed to analyze threads.")
        sys.exit(1)
    
    analyzed_count = len(analysis) if isinstance(analysis, list) else 0
    print(f"         Analyzed {analyzed_count} threads.")

    # Step 2: Export to CSV
    print(f"Step 2/2: Exporting CSV to: {args.output}")
    export_to_csv(analysis, args.output)
    print(f"\nDone! CSV saved to: {args.output}")

if __name__ == "__main__":
    main()
