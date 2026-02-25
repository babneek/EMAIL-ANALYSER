"""
Thread Analyzer — calls OpenAI to perform deep analytics on each thread.
Mirror of SimplAI Node 3 (Thread_Analyzer).
"""

import json
from openai import OpenAI

SYSTEM_PROMPT = """You are a sales intelligence analyst. You analyze email threads for sentiment, client requirements, sales rep performance, and risk. Return ONLY valid JSON, no markdown code blocks."""

USER_PROMPT_TEMPLATE = """Analyze each email thread below and produce a detailed assessment.

Threads:
{threads}

For EACH thread, evaluate:

1. **Sentiment**: Overall sentiment (Positive / Neutral / Negative) and trend (Improving / Stable / Declining).
2. **Client Requirements**: What does the client need? List explicit and implicit requirements.
3. **Open Questions**: Unresolved questions the client has asked.
4. **Sales Rep Understanding**: Did the rep clearly understand the client's needs? (Clear / Partial / Poor). Identify gaps like unanswered questions, repeated follow-ups, or vague responses.
5. **Risk Level**: Low / Medium / High — based on unresolved issues, negative sentiment, or dropped threads.
6. **Recommended Next Action**: What should the sales team do next?

Return ONLY this JSON structure:
{{
  "analyzed_threads": [
    {{
      "thread_id": "T001",
      "conversation_id": "CONV_001",
      "thread_topic": "Pricing",
      "email_count": 3,
      "participants": "alice@client.com; bob@sales.com",
      "overall_sentiment": "Negative",
      "sentiment_trend": "Declining",
      "client_requirements": "Wants 20% volume discount for 500+ licenses; needs pricing locked for 2 years",
      "open_questions": "What is the discount for annual vs monthly billing?",
      "sales_rep_understanding": "Partial",
      "sales_rep_gaps": "Did not address the 2-year price lock request; repeated client follow-up on discount tiers",
      "risk_level": "High",
      "recommended_next_action": "Schedule pricing call; prepare custom discount proposal for 500+ licenses",
      "last_updated": "2026-02-20T14:30:00Z"
    }}
  ]
}}

Rules:
- One object per thread. Do not merge threads.
- "participants" should be a semicolon-separated string.
- "client_requirements", "open_questions", "sales_rep_gaps" should be concise semicolon-separated strings.
- "last_updated" should be the timestamp of the latest email in the thread.
- Output raw JSON only."""


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
