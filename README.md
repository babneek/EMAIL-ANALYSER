# Sales Email Thread Analytics

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://email-analytics-jm325eketabavr9apkcxo5.streamlit.app/)

**[Live Demo on Streamlit Cloud](https://email-analytics-jm325eketabavr9apkcxo5.streamlit.app/)**

An AI-powered application that analyzes sales email conversations and converts unstructured email data into structured CSV outputs. It identifies discussion threads, analyzes sentiment, extracts requirements, and evaluates sales representative performance.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API Key

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install streamlit openai pandas python-dotenv
   ```
3. Set up your environment:
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

## 🛠️ Usage

### 1. Streamlit Web App (Recommended)
The premium web interface allows you to upload JSON files, visualize the analysis, and download the CSV report.
```bash
streamlit run app/streamlit_app.py
```

### 2. Command Line Interface
Run the analysis directly from your terminal.
```bash
python app/main.py --input sample_emails.json --output report.csv
```

## 📂 Project Structure
- `app/streamlit_app.py`: Premium Streamlit dashboard.
- `app/main.py`: CLI entry point.
- `app/thread_identifier.py`: Logic for grouping emails into threads.
- `app/thread_analyzer.py`: Logic for sentiment, risk, and gap analysis.
- `app/csv_exporter.py`: Utility for CSV generation.
- `sample_emails.json`: Example dataset for testing.

## 📊 Output Schema
The final CSV contains 14 attributes including:
- `thread_id`: Unique identifier for the thread
- `overall_sentiment`: Positive / Neutral / Negative
- `risk_level`: Low / Medium / High
- `sales_rep_understanding`: Clear / Partial / Poor
- `recommended_next_action`: Suggested follow-up
... and more.

## 📄 Documentation
For detailed information on the AI logic and SimplAI nodes, see [documentation.md](documentation.md).
