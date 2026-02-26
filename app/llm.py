import json
import os
from groq import Groq

def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=api_key)

def identify_threads(emails_json: str, api_key: str = None, model: str = "llama-3.1-8b-instant", verbose: bool = False) -> dict:
    SYSTEM_PROMPT = """You are an expert email analyst. Your job is to identify distinct discussion threads within sales email conversations. Return ONLY valid JSON, no markdown code blocks, no explanations."""
    USER_PROMPT_TEMPLATE = """Analyze the following sales email conversations and identify all distinct discussion threads.

Emails:
{emails}

Group the emails by discussion thread. A thread is defined by a specific topic (e.g., Pricing, Product Features, Timeline, Contract Terms). A single email may belong to multiple threads if it discusses multiple topics.

Return ONLY this JSON structure:
{{
  "threads": [
    {{
      "thread_id": "T001",
      "conversation_id": "CONV_001",
      "thread_topic": "Short descriptive label",
      "email_ids": ["E001", "E003", "E007"],
      "participants": ["sender1@example.com", "sender2@example.com"],
      "email_count": 3,
      "emails_content": [
        {{
          "email_id": "E001",
          "sender": "...",
          "timestamp": "...",
          "relevant_excerpt": "The portion of this email relevant to this thread"
        }}
      ]
    }}
  ]
}}

Rules:
- Every email must appear in at least one thread.
- Thread topics should be specific labels like: Pricing, Product Features, Implementation Timeline, Contract Terms, Support SLAs, Data Migration, Security Compliance, etc.
- Output raw JSON only."""
    
    client = get_client()
    user_prompt = USER_PROMPT_TEMPLATE.format(emails=emails_json)
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
        return json.loads(content)
    except Exception as e:
        print(f"ERROR in thread identification: {e}")
        return None

def analyze_threads(threads_json: str, api_key: str = None, model: str = "llama-3.1-8b-instant", verbose: bool = False) -> dict:
    SYSTEM_PROMPT = """You are a "Zero-Mercy" sales intelligence analyst. Your job is to perform deep reasoning on email threads to identify exactly where sales representatives failed to address client requirements. You are looking for missed opportunities, unanswered questions, and lack of follow-through. Return ONLY valid JSON, no markdown code blocks."""
    USER_PROMPT_TEMPLATE = """Perform a "Zero-Mercy" gap analysis on each email thread below. Produce a detailed assessment focusing on performance gaps.

Threads:
{threads}

For EACH thread, evaluate:

1. **Sentiment**: Overall sentiment (Positive / Neutral / Negative) and trend (Improving / Stable / Declining).
2. **Client Requirements**: What does the client need? List explicit and implicit requirements.
3. **Open Questions**: Unresolved questions the client has asked.
4. **Sales Rep Understanding**: (Clear / Partial / Poor). Identify exactly which questions were ignored or answered vaguely.
5. **Sales Rep Gaps**: LIST EVERY PIECE OF INFORMATION OR ACTION THE REP FAILED TO PROVIDE. Be specific.
6. **Risk Level**: Low / Medium / High.
7. **Recommended Next Action**: Immediate corrective action.

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
      "sales_rep_gaps": "Ignored 2-year price lock request; failed to provide annual vs monthly billing breakdown; did not confirm if 20% discount applies to first year only",
      "risk_level": "High",
      "recommended_next_action": "Send comprehensive pricing matrix with 2-year lock confirmation",
      "last_updated": "2026-02-20T14:30:00Z"
    }}
  ]
}}

Rules:
- One object per thread.
- "participants" should be a semicolon-separated string.
- "client_requirements", "open_questions", "sales_rep_gaps" must be detailed semicolon-separated strings.
- "last_updated" must be the timestamp of the very last email.
- Output raw JSON only."""
    
    client = get_client()
    user_prompt = USER_PROMPT_TEMPLATE.format(threads=threads_json)
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
        return json.loads(content)
    except Exception as e:
        print(f"ERROR in thread analysis: {e}")
        return None