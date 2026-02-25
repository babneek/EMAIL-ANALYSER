#!/usr/bin/env python3
"""
Sales Email Thread Analytics — CLI Application
Usage: python main.py --input sample_emails.json --output report.csv
"""

import argparse
import json
import sys
import os
from dotenv import load_dotenv

from thread_identifier import identify_threads
from thread_analyzer import analyze_threads
from csv_exporter import export_to_csv

load_dotenv()


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
        default=os.getenv("MODEL_NAME", "gpt-4o-mini"),
        help=f"OpenAI model to use (default: {os.getenv('MODEL_NAME', 'gpt-4o-mini')})"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed progress output"
    )

    args = parser.parse_args()

    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found. Set it in .env file or environment.")
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

    emails_json = json.dumps(emails_data)

    # Step 1: Identify threads
    print("Step 1/3: Identifying email threads...")
    threads = identify_threads(emails_json, api_key, args.model, args.verbose)
    if not threads:
        print("ERROR: Failed to identify threads.")
        sys.exit(1)
    thread_count = len(threads.get("threads", []))
    print(f"         Found {thread_count} threads.")

    # Step 2: Analyze threads
    print("Step 2/3: Analyzing threads (sentiment, risk, requirements)...")
    analysis = analyze_threads(json.dumps(threads), api_key, args.model, args.verbose)
    if not analysis:
        print("ERROR: Failed to analyze threads.")
        sys.exit(1)
    analyzed_count = len(analysis.get("analyzed_threads", []))
    print(f"         Analyzed {analyzed_count} threads.")

    # Step 3: Export to CSV
    print(f"Step 3/3: Exporting CSV to: {args.output}")
    export_to_csv(analysis, args.output)
    print(f"\nDone! CSV saved to: {args.output}")
    print(f"Rows: {analyzed_count} threads | Columns: 14 attributes")


if __name__ == "__main__":
    main()
