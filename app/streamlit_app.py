import streamlit as st
import json
import pandas as pd
import os
from io import BytesIO, StringIO
from dotenv import load_dotenv

# Import our logic modules
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from thread_identifier import identify_threads
from thread_analyzer import analyze_threads
from csv_exporter import export_to_csv

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="Sales Insights Engine",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Outfit:wght@700&display=swap');

    :root {
        --primary: #2563eb;
        --primary-dark: #1e40af;
        --secondary: #64748b;
        --accent: #f59e0b;
        --bg-light: #f8fafc;
        --card-bg: #ffffff;
    }

    .main {
        background-color: var(--bg-light);
    }

    /* Global Typography */
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
    }

    /* Header Styling */
    .stTitle {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3.5rem !important;
        padding-bottom: 0.5rem;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        color: white;
    }
    
    /* Custom Container/Card */
    .custom-card {
        background: white;
        padding: 2.5rem;
        border-radius: 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 20px -5px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
    }

    /* Premium Button Styling */
    div.stButton > button {
        width: 100%;
        border-radius: 14px;
        height: 3.8rem;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white !important;
        font-weight: 700;
        font-size: 1.2rem;
        border: none;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 20px -3px rgba(37, 99, 235, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(37, 99, 235, 0.4);
        border: none;
        color: white !important;
    }
    
    /* Secondary/Form Button */
    div[data-testid="stForm"] div.stButton > button {
        height: 3rem;
        background: #f1f5f9;
        color: #1e293b !important;
        box-shadow: none;
        text-transform: none;
        font-size: 1rem;
        border: 1px solid #e2e8f0;
    }
    
    div[data-testid="stForm"] div.stButton > button:hover {
        background: #e2e8f0;
        color: #0f172a !important;
        transform: translateY(-2px);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 1.1rem;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Session State
if 'data' not in st.session_state: st.session_state.data = None
if 'df' not in st.session_state: st.session_state.df = None

# Sidebar
with st.sidebar:
    st.markdown("<div style='text-align: center; padding-top: 2rem;'>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/96/000000/analytics.png", width=80)
    st.markdown("<h2 style='color:white;'>Sales Insights</h2>", unsafe_allow_html=True)
    st.write("v1.0.0")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.write("Model: `gpt-4o-mini`")

# Header
st.markdown("""
<div style='background: white; padding: 3rem; border-radius: 30px; border: 1px solid #e2e8f0; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);'>
    <h1 style='margin:0; font-family: Outfit; font-size: 3.5rem;'>Sales Intelligence Engine</h1>
    <p style='color: #64748b; font-size: 1.4rem; margin-top: 1rem;'>
        Transform unstructured email data into executive analytics.
    </p>
</div>
""", unsafe_allow_html=True)

# Main Card
st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
st.markdown("### 📥 Load Conversations")
t1, t2, t3 = st.tabs(["📁 File Upload", "📋 Direct Paste", "💡 Demo Data"])

with t1:
    up = st.file_uploader("Upload email JSON", type=["json"], label_visibility="collapsed")
    if up:
        try:
            st.session_state.data = json.loads(up.read().decode())
            st.success("File loaded successfully.")
        except: st.error("Invalid JSON file.")

with t2:
    with st.form("p"):
        txt = st.text_area("Paste JSON here", height=200, label_visibility="collapsed", placeholder="Paste conversation JSON...")
        if st.form_submit_button("💾 Apply Current Snippet"):
            try:
                st.session_state.data = json.loads(txt)
                st.success("Snippet applied manually.")
            except: st.error("Invalid JSON syntax.")

with t3:
    st.markdown("<div style='text-align: center; padding: 1.5rem;'>", unsafe_allow_html=True)
    st.write("Use our pre-configured sample dataset to see the engine in action.")
    if st.button("✨ Load Sample Emails"):
        sample_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_emails.json")
        try:
            with open(sample_path, "r") as f:
                st.session_state.data = json.load(f)
                st.success("Sample emails loaded! Scroll down to run analysis.")
        except Exception as e:
            st.error(f"Could not find sample_emails.json at {sample_path}")
    st.markdown("</div>", unsafe_allow_html=True)

# Execution
if st.session_state.data:
    st.markdown("---")
    if st.button("🚀 EXECUTE DEEP ANALYSIS ENGINE"):
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("MODEL_NAME", "gpt-4o-mini")
        
        if not api_key: st.error("API Key not found in .env")
        else:
            with st.status("🧠 Processing Analysis...", expanded=True) as status:
                st.write("🧵 Mapping threads...")
                threads = identify_threads(json.dumps(st.session_state.data), api_key, model)
                
                if threads and "threads" in threads:
                    st.write("📊 Analyzing sentiment and risks...")
                    analysis = analyze_threads(json.dumps(threads), api_key, model)
                    
                    if analysis and "analyzed_threads" in analysis:
                        rows = []
                        cols = ['thread_id', 'conversation_id', 'thread_topic', 'email_count', 'participants', 'overall_sentiment', 'sentiment_trend', 'client_requirements', 'open_questions', 'sales_rep_understanding', 'sales_rep_gaps', 'risk_level', 'recommended_next_action', 'last_updated']
                        for t in analysis["analyzed_threads"]:
                            rows.append({c: ("; ".join(map(str, t.get(c, []))) if isinstance(t.get(c), list) else t.get(c, '')) for c in cols})
                        st.session_state.df = pd.DataFrame(rows)
                        status.update(label="✅ Analysis Complete!", state="complete")
                    else: st.error("Analysis failed.")
                else: st.error("Mapping failed.")

st.markdown("</div>", unsafe_allow_html=True)

# Dashboard
if st.session_state.df is not None:
    df = st.session_state.df
    st.markdown("### 📈 Dashboard Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Active Threads", len(df))
    hr = len(df[df['risk_level'].str.lower().str.contains('high|critical')])
    c2.metric("Critical Risks", hr, delta="- Urgent" if hr > 0 else "None")
    c3.metric("Core Mood", df['overall_sentiment'].mode()[0].capitalize())

    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.dataframe(df, width='stretch', hide_index=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button("📥 DOWNLOAD CSV REPORT", df.to_csv(index=False).encode('utf-8'), "sales_report.csv", "text/csv", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.data:
    st.markdown("<div style='text-align: center; color: #94a3b8; padding: 4rem;'>Awaiting data source...</div>", unsafe_allow_html=True)
