from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os
from ..core.analyzer import analyze_threads
from ..utils.csv_exporter import analysis_to_csv

router = APIRouter()

class AnalyzeRequest(BaseModel):
    emails_text: str
    model: str = "llama-3.1-8b-instant"

@router.post("/analyze")
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

    # Perform Analysis
    analysis = analyze_threads(clean_txt, groq_api_key, request.model)
    if not analysis or not isinstance(analysis, list):
        raise HTTPException(status_code=500, detail="Failed to perform thread analysis")

    # Prepare CSV Data
    csv_data = analysis_to_csv(analysis)

    return {
        "threads": analysis, 
        "analysis": analysis,
        "csv": csv_data
    }
