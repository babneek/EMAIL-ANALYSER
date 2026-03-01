# 📧 SimplAI Email Intelligence Analytics

> **High-Reasoning Sales Operations Agent with Zero-Mercy Gap Analysis**

SimplAI Email Analytics is a professional-grade intelligence platform designed to extract, analyze, and audit sales email conversations. Using advanced LLM reasoning (Groq/Llama-3), it identifies discussion threads and performs rigorous "Zero-Mercy" gap detection to help sales managers identify where representatives are missing critical client requirements.

---

## 🔗 Live Application
Access the production dashboard here:
- **Sales Email Intelligence application**: [https://email-analytics-dashboard-q3nc.onrender.com](https://email-analytics-dashboard-q3nc.onrender.com)

---

## 🏗️ Project Architecture

```text
simplai-email-analytics/
├── backend/                # FastAPI High-Performance Server
│   ├── app/                # Main Application Package
│   │   ├── api/            # API Route Handlers
│   │   ├── core/           # Business & AI Logic (LLM)
│   │   └── utils/          # Export & Formatting Utilities
│   ├── scripts/            # CLI Tools & Automation Scripts
│   ├── tests/              # Test Suites & Sample Data
├── frontend/               # React + Vite + Framer Motion Dashboard
│   ├── src/
│   │   ├── components/     # UI Architecture
│   │   └── services/       # API Abstraction Layer
└── README.md               # Project Entry Point
```

---

## 🚀 Getting Started

### 1. Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your environment: `cp .env.example .env` and add your `GROQ_API_KEY`.
4. Start the server: `uvicorn app.main:app --reload`

### 2. Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the dev server: `npm run dev`
4. Access the dashboard at `http://localhost:5173`.

---

## 🛠️ Key Features

### 🔍 Zero-Mercy Analysis
The core intelligence engine doesn't just summarize; it **audits**. 
- **Missed Detail Gaps**: Any specific requirement ignored by the rep.
- **Sentiment Slippage**: Negative trends in client communication.
- **Risk Identification**: Automated high-risk flagging for at-risk deals.

### 📊 Multi-Channel Output
- **Interactive Dashboard**: Real-time analysis with Framer Motion animations.
- **CSV Professional Export**: Generate management-ready reports in seconds.
- **CLI Power Tool**: Batch process data via the command line.

---

## 💻 CLI Usage
```bash
python backend/scripts/cli.py --input backend/tests/data/sample_emails.json --output report.csv
```

---

Built with ❤️ by **SimplAI Systems**
