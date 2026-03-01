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
- If an email contains a specific question, ensure the "relevant_excerpt" includes that exact question.
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
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"ERROR in thread identification: {e}")
        return None

def analyze_threads(emails_text: str, api_key: str = None, model: str = "llama-3.1-8b-instant", verbose: bool = False) -> list:
    SYSTEM_PROMPT = """You are a Lead Sales Operations Analyst. Your role is "Zero-Mercy" gap detection.
    
    STRICT GROUNDING RULE: Only create entries for topics that are EXPLICITLY discussed in the provided email text. 
    If a topic is not in the text, do NOT create a row for it.
    
    EXPERT ANALYTICAL ROLE: Cross-reference every client request against every representative response. 
    If a rep missed even a tiny detail (like a specific discount percentage or a report request), you MUST flag it as a 'Gap'.
    Set 'sales_rep_understanding' to 'Poor' or 'Partial' if any client question was ignored or answered vaguely.
    Set 'risk_level' to 'High' if critical questions were ignored or sentiment is 'Negative'.
    """

    USER_PROMPT = f"""THE ULTIMATE SALES INTELLIGENCE PROMPT
    
    CRITICAL FORMATTING RULES:
    1. Array Output: You MUST return a JSON ARRAY of objects. Each row in the final CSV must be its own object in the array.
    2. One Topic Per Object: If a conversation covers Pricing, Security, and SLAs, you must create 3 separate objects. NEVER merge topics.
    3. No Markdown: Return RAW JSON ONLY. Do not use ```json or any backticks.
    4. Consistency: Use 'N/A' or 'None' for empty fields. Do not omit any of the 14 attributes.

    EXPLICIT ATTRIBUTE DEFINITIONS: strictly populate these 14 attributes as defined below:
    - thread_id: Generate a strict serial ID. Format: THR_001_1, THR_001_2, etc.
    - conversation_id: Use the ID from the dataset if available, otherwise CONV_001.
    - thread_topic: Professional, specific label (e.g., "Pricing Negotiation", "API Error Troubleshooting").
    - email_count: The total count (Integer) of emails belonging to this specific thread.
    - participants: Semicolon-separated list of all email addresses involved.
    - overall_sentiment: Exactly one of: [Positive, Neutral, Negative].
    - sentiment_trend: Exactly one of: [Improving, Stable, Declining].
    - client_requirements: Semicolon-separated list of every explicit or implicit need.
    - open_questions: Semicolon-separated list of unresolved questions.
    - sales_rep_understanding: Exactly one of: [Clear, Partial, Poor].
    - sales_rep_gaps: Detailed, semicolon-separated list of exactly what the representative missed, ignored, or answered vaguely. BE CRITICAL.
    - risk_level: Exactly one of: [Low, Medium, High].
    - recommended_next_action: A single, clear, actionable instruction to fix the identified gaps.
    - last_updated: The ISO timestamp of the very latest email within this specific thread.

    DATASET TO ANALYZE:
    {emails_text}
    """
    
    client = get_client()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT}
            ],
            temperature=0.0,
            # Groq supports json_object, but for a list we should be careful. 
            # However, the prompt is very strict.
        )
        content = response.choices[0].message.content.strip()
        # Remove markdown if the model hallucinated it
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
            if content.startswith("json"):
                content = content[4:].strip()
                
        return json.loads(content)
    except Exception as e:
        print(f"ERROR in ultimate analysis: {e}")
        return None