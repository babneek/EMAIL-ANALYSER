"""
Thread Identifier — calls OpenAI to group emails into conversation threads.
Mirror of SimplAI Node 2 (Thread_Identifier).
"""

import json
from openai import OpenAI

SYSTEM_PROMPT = """You are an expert sales email analyst. Your task is to analyze a collection of sales emails and identify distinct conversation threads.

For each thread, extract:
- A unique thread_id (e.g., T001, T002)
- The conversation_id it belongs to
- A descriptive thread_topic
- The email_ids that belong to this thread
- All participants involved

Group emails by their actual topic/subject matter, not just by reply chain.
A single conversation may contain multiple threads (pricing, implementation, support, etc.).

Return ONLY valid JSON in this exact format:
{
  "threads": [
    {
      "thread_id": "T001",
      "conversation_id": "CONV_001",
      "thread_topic": "Topic description",
      "email_ids": ["E001", "E002"],
      "participants": ["Name1 <email1>", "Name2 <email2>"]
    }
  ]
}"""

USER_PROMPT_TEMPLATE = """Analyze these sales emails and identify all distinct conversation threads:

{emails}

Group them by topic/discussion thread and return the structured JSON."""


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
