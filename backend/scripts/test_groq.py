import os
import json
import sys
from dotenv import load_dotenv

# Add app to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))
from llm import identify_threads

load_dotenv()

def test():
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")
    
    with open("test_emails.json", "r") as f:
        emails = f.read()
    
    print(f"Testing with model: {model}")
    try:
        threads = identify_threads(emails, api_key, model)
        print("Result:")
        print(json.dumps(threads, indent=2))
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test()
