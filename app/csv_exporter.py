import csv
import json
import os

def export_to_csv(analysis_data, output_file):
    """
    Exports analyzed threads to a CSV file.
    
    analysis_data: dict with 'analyzed_threads' key
    output_file: path to save the CSV
    """
    # Define CSV columns based on requirement
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
    
    threads = analysis_data.get('analyzed_threads', [])
    
    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for thread in threads:
                # Prepare row, ensuring lists are converted to strings
                row = {}
                for field in fieldnames:
                    val = thread.get(field, '')
                    if isinstance(val, list):
                        row[field] = "; ".join(map(str, val))
                    else:
                        row[field] = val
                writer.writerow(row)
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False
