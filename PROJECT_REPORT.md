# Assignment One: Sales Email Intelligence Systems

## 1. Installation & Setup
To get started with the source code and local project resources, clone the repository and navigate into the project directory:

```bash
git clone https://github.com/babneek/EMAIL-ANALYSER.git
cd EMAIL-ANALYSER
```

## 2. Introduction
This project presents two distinct, high-performance implementations of a Sales Email Analytics system. The goal of both systems is to ingest unstructured email conversations, identify distinct discussion threads, and extract critical business intelligence—specifically detecting performance gaps where sales representatives fail to address client requirements.

---

## PART 1: React & FastAPI Intelligence Dashboard (High-Scale Dashboard)

### 1.1 Overview
The Web Application has been upgraded from a basic Streamlit app to a professional React-based enterprise dashboard. It mirrors the high-performance reasoning of the n8n agent by using the Groq LPU engine for near-instant analysis.

### 1.2 Tech Stack
- **Frontend/UI**: React 19 (Vite) + Framer Motion (Animations)
- **Backend/API**: FastAPI (Python)
- **AI Engine**: Groq (LPU Hardware)
- **Large Language Model**: Llama 3.3 70B Versatile
- **Data Engineering**: Pandas & Pydantic
- **Deployment**: Render (Static Site + Web Service)

### 1.3 System Architecture
The application follows a decoupled modern architecture:
- **`frontend/src/App.jsx`**: The React state controller and interactive UI.
- **`backend/api.py`**: The FastAPI server handling ingestion and AI orchestration.
- **`app/llm.py`**: The "Zero-Mercy" reasoning engine powering both thread identification and gap analysis.
- **`app/parser_to_csv.py`**: High-performance data transformation for reporting.

### 1.4 User Workflow
Users paste raw text or JSON $\rightarrow$ System cleanses ingestion $\rightarrow$ Groq performs 70B reasoning $\rightarrow$ Gaps are visualized in a glassmorphic table $\rightarrow$ Immediate CSV download.

---

## PART 2: n8n Intelligent Automation Agent (No-Code Pipeline)

### 2.1 Overview
The n8n implementation is built for high-scale automation. It is a "Zero-Click" agent that processes data via webhooks and handles both structured JSON and raw, copy-pasted text from any platform (Outlook, Gmail, Slack).

### 2.2 Tech Stack
- **Orchestration**: n8n Workflow Automation
- **AI Engine**: Groq (LPU Hardware)
- **Large Language Model**: Llama 3.3 70B Versatile
- **Logic Layer**: JavaScript (Custom Node.js execution)

### 2.3 Workflow Pipeline
1. **Intelligent Ingestion**: A "General Text Parser" uses JavaScript to sanitize inputs, removing hidden characters and BOM markers to ensure 100% JSON reliability.
2. **Deep Reasoning**: A "Master Prompt" instructs the AI to perform "Zero-Mercy" gap analysis, identifying exactly which questions the sales rep failed to answer.
3. **ID Sanitization**: Custom logic prevents AI hallucinations by forcing machine-readable IDs (e.g., `THR_001_1`).
4. **Mandatory 14-Column Schema**:
   Extracts `thread_id`, `conversation_id`, `thread_topic`, `email_count`, `participants`, `overall_sentiment`, `sentiment_trend`, `client_requirements`, `open_questions`, `sales_rep_understanding`, `sales_rep_gaps`, `risk_level`, `recommended_next_action`, and `last_updated`.

### 2.4 Deliverable
The agent automatically triggers a browser-side CSV download via a **Respond to Webhook** node, providing immediate reporting with no manual intervention.

---

## 3. Comparison & Conclusion
Previously, the Web App and n8n Agent used different logic. Now, **both are unified**. The Web App now runs on the same **Groq + Llama 3.3** engine as the n8n agent, providing consistent "Zero-Mercy" gap analysis across all interfaces.

---

# Assignment Two: Lead Generation Intelligence System

## 1. Project Goal
Build a Lead Generation System to find emails, phone numbers, and LinkedIn profiles of founders/CEOs/co-founders.
- **Input**: List of companies with Company Name, Person Name, Position, LinkedIn URL.
- **Output**: Verified contact information suitable for business outreach.

### Sample Input Data:
| Company | Person Name | Position | LinkedIn |
| :--- | :--- | :--- | :--- |
| Sarvam AI | Vivek Raghavan | CEO, Founder | [LinkedIn](https://linkedin.com/company/sarvam-ai) |
| Vedantu | Vedant Khanduri | CEO, Founder | [LinkedIn](https://linkedin.com/company/vedantu) |

## 2. Tools & Methods Attempted

| Tool / Approach | Method / Settings | Key Findings |
| :--- | :--- | :--- |
| **OpenAI GPT Models** | **GPT-4o-mini (Temp: 0.1)** | ✅ Superior performance. By switching from Sarvam to GPT-4o-mini with a very low temperature (0.1), I achieved near-zero hallucination rates and significantly more accurate real-time data retrieval. |
| **Sarvam AI API** | n8n Workflow Parsing | ✅ Reliable, but less flexible for real-time edge cases compared to GPT-4o-mini. |
| **Apollo.io API** | n8n HTTP Request | ❌ Automated enrichment is restricted on free plans; requires paid API key for full agent integration. |
| **SignalHire** | Chrome Extension | ✅ Proved successful for manual retrieval of phone numbers/emails using free credits. |
| **LinkedIn Scraping** | Python / n8n Nodes | ❌ Highly unstable due to advanced anti-scraping measures; not recommended for high-reliability production. |

## 3. n8n Implementation & Strategy
1. **Model Optimization**: I transitioned to **GPT-4o-mini** with a temperature of **0.1**. This was a pivotal change that ensured the data mapping was highly grounded in reality and provided a more robust logic for handling person-to-company relationships.
2. **Data Architecting**: Developed a flow to flatten company JSON objects into clean, single-row entities.
3. **Contact Prioritization**: Implemented logic to intelligently select the "Primary Contact" based on seniority (CEO > Founder > Co-Founder).
4. **Agent-Ready Hooks**: Although full automation is blocked by free-tier API restrictions, the n8n agent is architecturally "plug-and-play" ready for **Apollo** or **SignalHire** once professional API keys are applied.

## 4. Technical Discoveries & Barriers
While the logic for the agent is fully built, there were significant platform-level hurdles:
- **Enrichment Access**: My research confirmed that tools like **SignalHire** and **Apollo** work perfectly for retrieving phone numbers and emails via their web interfaces/credits. However, they strictly prohibit "Free Tier" users from accessing this data through their API (the method required for an automated Agent).
- **LinkedIn Anti-Scraping**: I attempted dedicated scraping nodes for LinkedIn, but the platform's security measures often led to inconsistent results. For a professional-grade agent, I believe using an official API aggregator is a more ethical and reliable path.
- **Agent Viability**: I am confident that by upgrading to a paid API license for any major data provider, this agent would transition from a "Logic Proof" to a "Fully Autonomous" system within minutes.

## 5. Proof of Concept (Manual Validation)
| Company | Person Name | Position | Email | Phone | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Sarvam AI | Vivek Raghavan | CEO | vivek@... | +91-XXXXXX | ✅ Verified (SignalHire) |

*Manual validation was performed to confirm that the lead data exists—further automated extraction simply awaits a production-grade API key.*

## 6. Closing Reflection
This project was an excellent challenge. It allowed me to deeply investigate the balance between **LLM reasoning** and **external API limitations**. While current free-tier restrictions prevent a "Zero-Click" automated enrichment for all leads, the underlying n8n logic and the refined GPT-4o-mini prompt system are prepared for full-scale production rollout. I believe this approach demonstrates a clear path toward a high-tier lead generation system.## 7. API Integration (The Webhook Layer)
To ensure these tools are production-ready, both systems are equipped with **Webhook Triggers** and **Webhook Responses**. This creates a true "Request-Response" cycle:

- **Sales Intelligence API**: Can be called via a POST request. The agent processes the emails and uses a **"Respond to Webhook"** node to immediately return the generated CSV file. This means an external app can call the URL and receive the physical file download as the direct response.
- **Lead Gen API**: Enables "Real-time Enrichment." A system sends a company name, and the agent uses a **"Respond to Webhook"** node to return the specific founder's validated contact data as a clean JSON response.

---

## 9. Live Application Access
The Sales Email Intelligence system is deployed and available via a secure web form. Users can paste their own email data (Standard Text or JSON) and receive an instantaneous CSV download of the analysis.

**🔗 [Launch Sales Intelligence Dashboard (Live)](https://email-analyser-dashboard.onrender.com)**

---

## 10. Final Project Resources
- **`node_prompts.md`**: Repository of all LLM prompts and JS snippets.
- **`big_test_data.json`**: Complex 9-email test dataset for stress testing.
- **`PROJECT_REPORT.md`**: This multi-assignment documentation.
