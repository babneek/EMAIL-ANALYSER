import csv
import io

def analysis_to_csv(analysis_data):
    """
    Converts analyzed threads to a CSV string.
    analysis_data: dict with 'analyzed_threads' key
    Returns: CSV string
    """
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
    if isinstance(analysis_data, list):
        threads = analysis_data
    else:
        threads = analysis_data.get('analyzed_threads', [])
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for t in threads:
        row = {c: ("; ".join(map(str, t.get(c, []))) if isinstance(t.get(c), list) else t.get(c, '')) for c in fieldnames}
        writer.writerow(row)
    return output.getvalue()