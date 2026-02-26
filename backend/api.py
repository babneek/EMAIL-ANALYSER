from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import sys
from dotenv import load_dotenv

# Ensure the 'app' directory is in the path so we can import llm.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))

from llm import identify_threads, analyze_threads
from parser_to_csv import analysis_to_csv

load_dotenv()

app = FastAPI(title="SimplAI Email Analytics API")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    emails_text: str
    model: str = "llama-3.3-70b-versatile"

@app.post("/analyze")
async def analyze_emails(request: AnalyzeRequest):
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not found in environment")

    # Clean input similar to the n8n "Intelligent Ingestion"
    clean_txt = request.emails_text.strip().replace('\ufeff', '')
    
    # Try to parse as JSON, if not, treat as raw text
    try:
        emails_obj = json.loads(clean_txt)
    except Exception:
        # Generic wrapper for raw text ingestion
        emails_obj = {
            "conversations": [
                {
                    "conversation_id": "CONV_RAW",
                    "emails": [{"email_id": "E1", "body": clean_txt}]
                }
            ]
        }

    # Step 1: Identify Threads
    threads = identify_threads(json.dumps(emails_obj), groq_api_key, request.model)
    if not threads or "threads" not in threads:
        raise HTTPException(status_code=500, detail="Failed to identify email threads")

    # Step 2: Analyze Threads (Zero-Mercy Gap Analysis)
    analysis = analyze_threads(json.dumps(threads), groq_api_key, request.model)
    if not analysis or "analyzed_threads" not in analysis:
        raise HTTPException(status_code=500, detail="Failed to perform thread analysis")

    # Step 3: Prepare CSV Data
    csv_data = analysis_to_csv(analysis)

    return {
        "threads": threads.get("threads", []),
        "analysis": analysis.get("analyzed_threads", []),
        "csv": csv_data
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
