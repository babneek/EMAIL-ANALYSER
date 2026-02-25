"""
Thread Identifier — calls OpenAI to group emails into conversation threads.
Mirror of SimplAI Node 2 (Thread_Identifier).
"""

import json
from openai import OpenAI

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


def identify_threads(emails_json: str, api_key: str, model: str = "gpt-4o-mini", verbose: bool = False) -> dict:
    """Call OpenAI to identify email threads. Returns parsed dict or None on failure."""
    client = OpenAI(api_key=api_key)

    user_prompt = USER_PROMPT_TEMPLATE.format(emails=emails_json)

    if verbose:
        print(f"  [Thread Identifier] Calling {model}...")

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
            print(f"  [Thread Identifier] Raw response:\n{content[:400]}...")

        result = json.loads(content)
        return result

    except Exception as e:
        print(f"  ERROR in thread identification: {e}")
        return None
