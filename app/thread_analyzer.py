"""
Thread Analyzer — calls OpenAI to perform deep analytics on each thread.
Mirror of SimplAI Node 3 (Thread_Analyzer).
"""

import json
from openai import OpenAI

SYSTEM_PROMPT = """You are an expert sales conversation analyst. Analyze each email thread and provide comprehensive insights.

For each thread, determine:
- overall_sentiment: positive / neutral / negative / mixed
- sentiment_trend: improving / declining / stable / volatile
- client_requirements: list of explicit requirements mentioned
- open_questions: list of unresolved questions or pending items
- sales_rep_understanding: how well the sales rep understands the client's needs
- sales_rep_gaps: areas where the sales rep missed or misunderstood requirements
- risk_level: low / medium / high / critical
- recommended_next_action: specific next step the sales team should take
- last_updated: timestamp or date of the most recent email in this thread

Return ONLY valid JSON in this exact format:
{
  "analyzed_threads": [
    {
      "thread_id": "T001",
      "conversation_id": "CONV_001",
      "thread_topic": "Topic description",
      "email_count": 3,
      "participants": ["Name1 <email1>", "Name2 <email2>"],
      "overall_sentiment": "positive",
      "sentiment_trend": "improving",
      "client_requirements": ["requirement 1", "requirement 2"],
      "open_questions": ["question 1", "question 2"],
      "sales_rep_understanding": "Brief assessment of understanding",
      "sales_rep_gaps": ["gap 1", "gap 2"],
      "risk_level": "low",
      "recommended_next_action": "Specific action to take",
      "last_updated": "2024-01-15"
    }
  ]
}"""

USER_PROMPT_TEMPLATE = """Perform comprehensive analysis on these identified email threads.
Use the thread structure below and infer content from the thread metadata and topics:

{threads}

For each thread, provide full analytical insights as specified. Return structured JSON."""


def analyze_threads(threads_json: str, api_key: str, model: str = "gpt-4o-mini", verbose: bool = False) -> dict:
    """Call OpenAI to analyze all threads. Returns parsed dict or None on failure."""
    client = OpenAI(api_key=api_key)

    user_prompt = USER_PROMPT_TEMPLATE.format(threads=threads_json)

    if verbose:
        print(f"  [Thread Analyzer] Calling {model}...")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        if verbose:
            print(f"  [Thread Analyzer] Raw response:\n{content[:400]}...")

        result = json.loads(content)
        return result

    except Exception as e:
        print(f"  ERROR in thread analysis: {e}")
        return None
