#!/usr/bin/env python3
"""
CSV Generator for SimplAI Email Thread Analytics
Converts Thread_Analyzer JSON output to CSV format
"""

import sys
import json
import csv
from io import StringIO


def clean_json_input(raw_input):
    """
    Remove markdown code fences if present in the input.
    SimplAI LLM nodes sometimes wrap JSON in ```json ... ```
    """
    cleaned = raw_input.strip()
    
    # Remove opening markdown fence
    if cleaned.startswith('```json'):
        cleaned = cleaned[7:]
    elif cleaned.startswith('```'):
        cleaned = cleaned[3:]
    
    # Remove closing markdown fence
    if cleaned.endswith('```'):
        cleaned = cleaned[:-3]
    
    return cleaned.strip()


def convert_to_csv(analyzed_threads):
    """
    Convert analyzed threads JSON to CSV format.
    
    Expected input structure:
    {
      "analyzed_threads": [
        {
          "thread_id": "T001",
          "conversation_id": "CONV_001",
          "thread_topic": "Pricing",
          "email_count": 3,
          "participants": "alice@client.com; bob@sales.com",
          "overall_sentiment": "Negative",
          "sentiment_trend": "Declining",
          "client_requirements": "Volume discount; 2-year price lock",
          "open_questions": "Annual pricing?",
          "sales_rep_understanding": "Partial",
          "sales_rep_gaps": "Missed price lock request",
          "risk_level": "High",
          "recommended_next_action": "Schedule call",
          "last_updated": "2026-02-20T14:30:00Z"
        }
      ]
    }
    """
    
    # Define CSV columns in order
    fieldnames = [
        'thread_id',
        'conversation_id',
        'thread_topic',
        'email_count',
        'participants',
        'overall_sentiment',
        'sentiment_trend',
        'client_requirements',
        'open_questions',
        'sales_rep_understanding',
        'sales_rep_gaps',
        'risk_level',
        'recommended_next_action',
        'last_updated'
    ]
    
    # Create CSV in memory
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    # Write header
    writer.writeheader()
    
    # Write data rows
    threads = analyzed_threads.get('analyzed_threads', [])
    for thread in threads:
        # Extract only the fields we need, in case there are extras
        row = {field: thread.get(field, '') for field in fieldnames}
        writer.writerow(row)
    
    return output.getvalue()


def main():
    """
    Main function - reads JSON from stdin, outputs CSV to stdout.
    This matches SimplAI's Python Code Node interface.
    """
    try:
        # Read all input from stdin
        raw_input = sys.stdin.read()
        
        if not raw_input.strip():
            print("Error: No input received", file=sys.stderr)
            sys.exit(1)
        
        # Clean markdown fences if present
        cleaned_input = clean_json_input(raw_input)
        
        # Parse JSON
        try:
            data = json.loads(cleaned_input)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON input - {e}", file=sys.stderr)
            print(f"Input received: {cleaned_input[:200]}", file=sys.stderr)
            sys.exit(1)
        
        # Convert to CSV
        csv_output = convert_to_csv(data)
        
        # Output to stdout (SimplAI captures this)
        print(csv_output, end='')
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
