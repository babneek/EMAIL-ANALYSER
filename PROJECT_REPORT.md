# Assignment Submission: Sales & Lead Generation Intelligence Systems

## 1. Project Overview
This project includes two AI-powered systems:
1. **Sales Email Intelligence System** – analyzes email conversations to detect gaps in sales performance.
2. **Lead Generation System** – finds verified emails, phone numbers, and LinkedIn profiles of company founders, CEOs, and co-founders.

Both systems combine AI reasoning with automated workflows for fast and accurate results.

---

## 2. Sales Email Intelligence System

### 2.1 Web Application (Streamlit Dashboard)
- **Purpose**: Allows sales managers to upload emails and view insights in an interactive dashboard.
- **Tech Stack**: Streamlit (UI), GPT-4o AI (analysis)
- **How it Works**:
  1. Users upload their email dataset.
  2. Emails are grouped into threads.
  3. AI analyzes each thread for sentiment, client requirements, and gaps in sales responses.
  4. Results can be downloaded as a CSV file for reporting.
- **Advantages**:
  - Real-time interactive dashboard
  - Easy visualization of gaps and risks
  - Manual review and export options

---

### 2.2 n8n Automation Agent (No-Code)
- **Purpose**: Fully automated analysis of sales emails with zero manual effort.
- **Tech Stack**: n8n, AI Engine (Groq / Llama 3.3 70B)
- **Workflow**:
  1. **Start Node** – Enter email data in any JSON format. For example:
```json
{
  "conversations": [
    {
      "conversation_id": "CONV_PRO_X",
      "client": "MacroSoft Global",
      "sales_rep": "Robert Parker",
      "emails": [
        {
          "email_id": "E_001",
          "sender": "vp_engineering@macrosoft.com",
          "recipient": "robert.p@salessolutions.com",
          "timestamp": "2026-02-15T09:00:00Z",
          "subject": "Infrastructure Upgrade Project - Initial Requirements",
          "body": "Hi Robert, following our call, we want to proceed with the Enterprise tier. We need: 1. 5000+ seats capacity. 2. Data residency strictly in Germany (EU). 3. 24/7 phone support with 1-hour SLA. 4. SSO integration with Azure AD. Can you confirm the total annual cost and confirm you meet these security requirements?"
        },
        {
          "email_id": "E_002",
          "sender": "robert.p@salessolutions.com",
          "recipient": "vp_engineering@macrosoft.com",
          "timestamp": "2026-02-15T10:30:00Z",
          "subject": "Re: Infrastructure Upgrade Project - Initial Requirements",
          "body": "Hi there! Great news. For 5000 seats, our list price is $25/user/month. Since you're a strategic account, I can offer 40% off. We support SSO perfectly. I'll send the contract today."
        }
      ]
    }
  ]
}
```
  2. **AI Node** – Detects unanswered client questions, gaps in sales responses, sentiment trends, and risk level.
  3. **Output Node** – Generates a structured CSV report with columns like Thread ID, Topic, Participants, Sentiment, Client Requirements, Open Questions, Sales Gaps, Risk Level, and Recommended Actions.
  4. **Delivery** – CSV is automatically sent/downloaded from the final node.

- **Advantages**:
  - Zero manual intervention
  - Fast, scalable, and accurate
  - Instant insights delivered via email

**How to test**:
- Simply enter your JSON emails in the start node.
- Run the workflow.
- Download your CSV report from the last node.

---

## 3. Lead Generation System (founder’s project)

### 3.1 Goal
Automatically find verified emails, phone numbers, and LinkedIn profiles of founders, CEOs, and co-founders based on company and person information.

### 3.2 Tools & Approach
- AI-driven reasoning using GPT-4o-mini (low temperature for accuracy)
- Prioritizes primary contacts (CEO > Founder > Co-Founder)
- Supports manual and automated validation of contact info
- n8n agents deliver the extracted contact info directly to emails

### 3.3 Challenges & Observations
- Free-tier APIs limit fully automated enrichment
- LinkedIn scraping is unreliable due to security restrictions
- Paid API access would make the system fully autonomous

**Proof of Concept**: Contacts were manually verified to ensure the system identifies correct emails and phone numbers.

---

## 4. API & Automation Integration
Both systems are webhook-enabled for real-time requests:
- **Sales Intelligence**: Accepts email data and returns analysis CSV
- **Lead Generation**: Accepts company/person info and delivers verified contact info via email

---

## 5. Conclusion
- The Sales Intelligence System helps managers detect gaps and risks in email communication.
- The Lead Generation System efficiently retrieves verified contact info for outreach.
- Together, these systems demonstrate how AI and automation can streamline sales operations and business development.

---

## Live Access:
- **Sales Email Intelligence application**: [https://email-analytics-dashboard-q3nc.onrender.com](https://email-analytics-dashboard-q3nc.onrender.com)
- **Both n8n agents**: Accessible on n8n (Invite sent to `sanyogeeta.dugar@simplai.ai`). Please check the "Shared with You" tab.
