# SimplAI Node Prompts — Copy-Paste Ready

This document contains all the prompts and configurations needed to build the Email Thread Analytics workflow on SimplAI.

---

## Node 1 — Start Point

**Configuration:**
- **Label:** Enter Email Conversations (JSON)
- **Variable Name:** `emails`
- **Type:** Text
- **Required:** Yes
- **Description:** Paste the contents of sample_emails.json here

**No prompts needed** — this is just an input node.

---

## Node 2 — Thread_Identifier (LLM Node)

**Configuration:**
- **Node Type:** LLM
- **Model:** `openai/gpt-4o-mini`
- **Temperature:** 0.2
- **Max Tokens:** 3000

### System Prompt

```
You are an expert email analyst. Your job is to identify distinct discussion threads within sales email conversations. Return ONLY valid JSON, no markdown code blocks, no explanations.
```

### User Prompt

```
Analyze the following sales email conversations and identify all distinct discussion threads.

Emails:
{{emails}}

Group the emails by discussion thread. A thread is defined by a specific topic (e.g., Pricing, Product Features, Timeline, Contract Terms). A single email may belong to multiple threads if it discusses multiple topics.

Return ONLY this JSON structure:
{
  "threads": [
    {
      "thread_id": "T001",
      "conversation_id": "CONV_001",
      "thread_topic": "Short descriptive label",
      "email_ids": ["E001", "E003", "E007"],
      "participants": ["sender1@example.com", "sender2@example.com"],
      "email_count": 3,
      "emails_content": [
        {
          "email_id": "E001",
          "sender": "...",
          "timestamp": "...",
          "relevant_excerpt": "The portion of this email relevant to this thread"
        }
      ]
    }
  ]
}

Rules:
- Every email must appear in at least one thread.
- Thread topics should be specific labels like: Pricing, Product Features, Implementation Timeline, Contract Terms, Support SLAs, Data Migration, Security Compliance, etc.
- Output raw JSON only.
```

---

## Node 3 — Thread_Analyzer (LLM Node)

**Configuration:**
- **Node Type:** LLM
- **Model:** `openai/gpt-4o-mini`
- **Temperature:** 0.2
- **Max Tokens:** 4000

### System Prompt

```
You are a sales intelligence analyst. You analyze email threads for sentiment, client requirements, sales rep performance, and risk. Return ONLY valid JSON, no markdown code blocks.
```

### User Prompt

```
Analyze each email thread below and produce a detailed assessment.

Threads:
{{Thread_Identifier.answer}}

For EACH thread, evaluate:

1. **Sentiment**: Overall sentiment (Positive / Neutral / Negative) and trend (Improving / Stable / Declining).
2. **Client Requirements**: What does the client need? List explicit and implicit requirements.
3. **Open Questions**: Unresolved questions the client has asked.
4. **Sales Rep Understanding**: Did the rep clearly understand the client's needs? (Clear / Partial / Poor). Identify gaps like unanswered questions, repeated follow-ups, or vague responses.
5. **Risk Level**: Low / Medium / High — based on unresolved issues, negative sentiment, or dropped threads.
6. **Recommended Next Action**: What should the sales team do next?

Return ONLY this JSON structure:
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
      "client_requirements": "Wants 20% volume discount for 500+ licenses; needs pricing locked for 2 years",
      "open_questions": "What is the discount for annual vs monthly billing?",
      "sales_rep_understanding": "Partial",
      "sales_rep_gaps": "Did not address the 2-year price lock request; repeated client follow-up on discount tiers",
      "risk_level": "High",
      "recommended_next_action": "Schedule pricing call; prepare custom discount proposal for 500+ licenses",
      "last_updated": "2026-02-20T14:30:00Z"
    }
  ]
}

Rules:
- One object per thread. Do not merge threads.
- "participants" should be a semicolon-separated string.
- "client_requirements", "open_questions", "sales_rep_gaps" should be concise semicolon-separated strings.
- "last_updated" should be the timestamp of the latest email in the thread.
- Output raw JSON only.
```

---

## Node 4 — CSV_Generator (Python Code Node)

**Configuration:**
- **Node Type:** Python Code
- **Python Version:** Python 3
- **Packages:** *(leave empty - uses only standard library)*
- **Input:** `{{Thread_Analyzer.answer}}`

### Python Code

Paste the entire contents of `csv_generator.py` into this node.

The script:
- Reads JSON from stdin
- Strips markdown code fences if present
- Converts to CSV with 14 columns
- Outputs CSV to stdout

---

## Node 5 — JSON to File Converter (Output Node)

**Configuration:**
- **Node Type:** JSON to File Converter
- **JSON Data:** `{{csv_generator.py.csv_data}}`
- **File Type:** CSV
- **File Name:** `email_thread_analytics.csv`

**Important:** Use `{{csv_generator.py.csv_data}}` to extract the CSV string from the Python node's JSON output.

---

## Connection Summary

```
Start Point (emails)
    ↓
Thread_Identifier (LLM)
    ↓ {{Thread_Identifier.answer}}
Thread_Analyzer (LLM)
    ↓ {{Thread_Analyzer.answer}}
csv_generator.py (Python)
    ↓ {{csv_generator.py.csv_data}}
JSON to File Converter (Output)
```

---

## Testing Tips

1. **Start small:** Test with just 3-4 emails first to verify the workflow
2. **Check each node:** After running, click on each node to see its output
3. **Common issues:**
   - LLM returns markdown code blocks → CSV_Generator handles this
   - Missing fields in JSON → Check Thread_Analyzer prompt
   - Empty output → Check that variable references match node names exactly

---

## Variable Reference Guide

| Node | Output Variable | Used By | Input From |
|------|----------------|---------|------------|
| Start Point | `{{emails}}` | Thread_Identifier | (user input) |
| Thread_Identifier | `{{Thread_Identifier.answer}}` | Thread_Analyzer | `{{emails}}` |
| Thread_Analyzer | `{{Thread_Analyzer.answer}}` | csv_generator.py | `{{Thread_Identifier.answer}}` |
| csv_generator.py | `{{csv_generator.py.csv_data}}` | JSON to File Converter | `{{Thread_Analyzer.answer}}` |
| JSON to File Converter | (downloadable file) | (end user) | `{{csv_generator.py.csv_data}}` |
