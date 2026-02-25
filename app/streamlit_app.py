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
    page_title="SimplAI | Sales Email Analytics",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded",
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
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p {
        color: #f1f5f9;
    }

    /* Custom Container/Card */
    .custom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }

    /* Premium Button Styling */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3rem;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-weight: 600;
        border: none;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2);
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(37, 99, 235, 0.3);
        border: none;
        color: white;
    }
    
    div.stButton > button:active {
        transform: translateY(0px);
    }

    /* Secondary/Validate Button */
    div[data-testid="stHorizontalBlock"] div.stButton > button {
        background: #f1f5f9;
        color: #1e293b;
        border: 1px solid #e2e8f0;
        box-shadow: none;
    }
    
    div[data-testid="stHorizontalBlock"] div.stButton > button:hover {
        background: #e2e8f0;
        color: #0f172a;
        border: 1px solid #cbd5e1;
    }

    /* Success/Validation message */
    .stAlert {
        border-radius: 12px;
        border: none;
    }

    /* Dataframe Styling */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }

    /* Metrics Styling */
    [data-testid="stMetric"] {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f1f5f9;
        border-radius: 10px 10px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }

    .stTabs [aria-selected="true"] {
        background-color: white !important;
        border-bottom: 2px solid var(--primary) !important;
    }
    
    /* Hide Deploy button and default headers */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<div style='text-align: center; padding: 1rem;'>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/96/000000/analytics.png", width=80)
    st.markdown("</div>", unsafe_allow_html=True)
    st.title("SimplAI Analytics")
    
    st.markdown("### 🛰️ System Status")
    api_key_status = "🟢 Configured" if os.getenv("OPENAI_API_KEY") else "🔴 Missing API Key"
    st.write(f"**Gateway:** {api_key_status}")
    
    model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
    st.write(f"**Intelligence:** `{model_name}`")
    
    st.markdown("---")
    
    # Advanced Settings
    with st.expander("🛠️ Advanced Settings"):
        api_key = st.text_input("Override API Key", value=os.getenv("OPENAI_API_KEY", ""), type="password")
        model = st.selectbox("LLM Model", ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"], index=0)
    
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY", "")
    if not model:
        model = os.getenv("MODEL_NAME", "gpt-4o-mini")

    st.markdown("### 📖 Guide")
    st.info("💡 **Pro-tip:** Use the 'Paste' option for quick snippets, or upload files for full conversation logs.")

# Header Section
st.markdown("""
    <div style='background: white; padding: 2rem; border-radius: 20px; border: 1px solid #e2e8f0; margin-bottom: 2rem;'>
        <h1 style='margin:0; font-family: Outfit;'>Sales Insights Engine</h1>
        <p style='color: #64748b; font-size: 1.1rem; margin-top: 0.5rem;'>
            Powered by SimplAI. Uncover threads, sentiment, and risks in seconds.
        </p>
    </div>
""", unsafe_allow_html=True)

# Input Section
st.markdown("### 📥 Source Selection")
tab1, tab2 = st.tabs(["📁 File Repository", "📋 Scratchpad / Paste"])

# Initialize session state for validation
if 'json_validated' not in st.session_state:
    st.session_state.json_validated = False
if 'last_input_hash' not in st.session_state:
    st.session_state.last_input_hash = None

current_input_data = None

with tab1:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Drop your conversation JSON here", type=["json"])
    if uploaded_file:
        try:
            content = uploaded_file.read().decode("utf-8")
            current_input_data = json.loads(content)
            col_v1, _ = st.columns([1, 3])
            with col_v1:
                if st.button("✨ Verify Payload", key="btn_check_file"):
                    st.session_state.json_validated = True
                    st.toast("Data Verified Successfully!", icon="🎉")
        except Exception as e:
            st.error(f"Error reading file: {e}")
            st.session_state.json_validated = False
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    json_text = st.text_area("JSON Code Snippet", height=250, placeholder="Paste JSON here...")
    if json_text:
        try:
            current_input_data = json.loads(json_text)
            col_v2, _ = st.columns([1, 3])
            with col_v2:
                if st.button("✨ Verify Syntax", key="btn_check_text"):
                    st.session_state.json_validated = True
                    st.toast("JSON Syntax Valid!", icon="✅")
        except json.JSONDecodeError as e:
            st.error(f"Syntax Error: {e}")
            st.session_state.json_validated = False
    st.markdown("</div>", unsafe_allow_html=True)

# Reset validation if input changes
input_hash = hash(str(current_input_data)) if current_input_data else None
if input_hash != st.session_state.last_input_hash:
    st.session_state.json_validated = False
    st.session_state.last_input_hash = input_hash

# Process Area
if current_input_data:
    st.markdown("---")
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        st.markdown("### 🏗️ Processing Console")
        with st.expander("📂 View Raw Structure"):
            st.json(current_input_data)
        
        if not st.session_state.json_validated:
            st.warning("⚠️ **Safety Check Required:** Please verify the payload above before activation.")
        
        # Primary Action Button
        run_btn = st.button("🚀 EXECUTE ANALYTICS ENGINE", 
                           disabled=not st.session_state.json_validated,
                           use_container_width=True)
        
        if run_btn:
            if not api_key:
                st.error("Missing Security Credential (API Key). Check .env or Sidebar.")
            else:
                ph = st.empty()
                with ph.container():
                    st.info("⚙️ Initializing Engine...")
                    p_bar = st.progress(0)
                    
                    # Step 1: Identification
                    st.write("🧵 Mapping Threads...")
                    p_bar.progress(20)
                    emails_json = json.dumps(current_input_data)
                    threads = identify_threads(emails_json, api_key, model, verbose=True)
                    
                    if threads and "threads" in threads:
                        # Step 2: Analysis
                        thread_count = len(threads["threads"])
                        st.write(f"✍️ Analyzing {thread_count} Threads...")
                        p_bar.progress(60)
                        analysis = analyze_threads(json.dumps(threads), api_key, model, verbose=True)
                        
                        if analysis and "analyzed_threads" in analysis:
                            p_bar.progress(90)
                            st.success("✅ Analysis Complete!")
                            
                            # Final Data Prep
                            df_rows = []
                            fieldnames = [
                                'thread_id', 'conversation_id', 'thread_topic', 'email_count', 
                                'participants', 'overall_sentiment', 'sentiment_trend', 
                                'client_requirements', 'open_questions', 'sales_rep_understanding', 
                                'sales_rep_gaps', 'risk_level', 'recommended_next_action', 'last_updated'
                            ]
                            
                            for thread in analysis["analyzed_threads"]:
                                row = {f: ("; ".join(map(str, thread.get(f, []))) if isinstance(thread.get(f), list) else thread.get(f, '')) for f in fieldnames}
                                df_rows.append(row)
                            
                            df = pd.DataFrame(df_rows)
                            st.session_state.df_result = df
                            p_bar.progress(100)
                            ph.empty()
                        else:
                            st.error("Analysis Engine Failure. check API limits.")
                    else:
                        st.error("Mapping Engine Failure. Check input format.")

    with col_b:
        st.markdown("### ℹ️ Operations Info")
        st.markdown("""
        - **Model:** `gpt-4o-mini`
        - **Latency:** ~5-15s
        - **Accuracy:** High
        - **Logic:** Sentiment, Gap Analysis, Risk Scoring
        """)

# Results Section
if 'df_result' in st.session_state:
    df = st.session_state.df_result
    st.markdown("---")
    st.markdown("### 📊 Intelligence Dashboard")
    
    # KPIs
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Captured Threads", len(df))
    high_risk = len(df[df['risk_level'].str.lower().str.contains('high|critical')])
    kpi2.metric("Critical Risks", high_risk, delta="- Action needed" if high_risk > 0 else "Safe")
    sentiment = df['overall_sentiment'].mode()[0] if not df.empty else "N/A"
    kpi3.metric("Lead Sentiment", sentiment.capitalize())
    
    # Data View
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Download
    csv_out = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 DOWNLOAD EXECUTIVE REPORT (CSV)",
        data=csv_out,
        file_name="sales_email_analysis.csv",
        mime="text/csv",
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Footer Info
if not current_input_data:
    st.markdown("""
    <div style='text-align: center; color: #94a3b8; padding: 3rem;'>
        <p>Awaiting data stream... Select a source to begin.</p>
    </div>
    """, unsafe_allow_html=True)
