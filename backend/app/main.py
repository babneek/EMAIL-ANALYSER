from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from dotenv import load_dotenv

# Ensure the root 'backend' directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Import API routes
from .api.routes import router as api_router

# Load .env from backend directory
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

app = FastAPI(title="SimplAI Email Analytics API")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    # Default port for development
    uvicorn.run(app, host="0.0.0.0", port=8000)
