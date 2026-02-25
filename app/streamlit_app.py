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
    page_title="Sales Email Analytics Engine",
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
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p {
        color: #f1f5f9;
        text-align: center;
    }

    /* Custom Container/Card */
    .custom-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 20px -5px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
    }

    /* Premium Button Styling */
    div.stButton > button {
        width: 100%;
        border-radius: 14px;
        height: 3.5rem;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        border: none;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        transform: translateY(-3px);
        box-shadow: 0 20px 25px -5px rgba(37, 99, 235, 0.4);
        border: none;
        color: white;
    }
    
    div.stButton > button:active {
        transform: translateY(0px);
    }

    /* Secondary Button (Confirm/Check) */
    .secondary-btn div.stButton > button {
        background: #f8fafc;
        color: #1e293b;
        border: 2px solid #e2e8f0;
        height: 3rem;
        box-shadow: none;
        text-transform: none;
        font-size: 1rem;
    }
    
    .secondary-btn div.stButton > button:hover {
        background: #f1f5f9;
        color: #0f172a;
        border: 2px solid #cbd5e1;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    /* Success/Validation message */
    .stAlert {
        border-radius: 12px;
        border: none;
    }

    /* Metrics Styling */
    [data-testid="stMetric"] {
        background: white;
        padding: 1.5rem;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: transparent;
        color: #64748b;
        font-weight: 600;
        font-size: 1rem;
    }

    .stTabs [aria-selected="true"] {
        color: var(--primary) !important;
        border-bottom: 3px solid var(--primary) !important;
    }

    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Sidebar (Branding Only)
with st.sidebar:
    st.markdown("<div style='text-align: center; padding: 2rem 1rem 1rem 1rem;'>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/96/000000/analytics.png", width=100)
    st.markdown("<h2 style='color:white; margin-top:1rem;'>Email Insights</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:0.9rem;'>Intelligence for modern sales teams.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🛠️ Mode")
    st.write(f"Active Engine: `gpt-4o-mini`")
    st.info("The application is running in fully automated mode using pre-configured system keys.")

# Header
st.markdown("""
    <div style='background: white; padding: 2.5rem; border-radius: 24px; border: 1px solid #e2e8f0; margin-bottom: 2rem; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);'>
        <h1 style='margin:0; font-family: Outfit; font-size: 3rem;'>Sales Intelligence Engine</h1>
        <p style='color: #64748b; font-size: 1.25rem; margin-top: 0.75rem; font-weight: 400;'>
            Extract threads, analyze sentiment, and pinpoint risks from your email conversations.
        </p>
    </div>
""", unsafe_allow_html=True)

# Sessions and logic
if 'json_validated' not in st.session_state:
    st.session_state.json_validated = False
if 'last_input_hash' not in st.session_state:
    st.session_state.last_input_hash = None
if 'df_result' not in st.session_state:
    st.session_state.df_result = None

current_input_data = None
api_key = os.getenv("OPENAI_API_KEY", "")
model = os.getenv("MODEL_NAME", "gpt-4o-mini")

# Main Input Card
st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
st.markdown("### 📥 Input Source")
tab1, tab2 = st.tabs(["📁 Upload Conversations", "📋 Paste Data Snippets"])

with tab1:
    uploaded_file = st.file_uploader("Drop your email conversation JSON here", type=["json"])
    if uploaded_file:
        try:
            content = uploaded_file.read().decode("utf-8")
            current_input_data = json.loads(content)
        except Exception as e:
            st.error(f"Error reading file: {e}")

with tab2:
    json_text = st.text_area("JSON Code Snippet", height=200, placeholder="Paste email JSON here...")
    if json_text:
        try:
            current_input_data = json.loads(json_text)
        except json.JSONDecodeError as e:
            st.error(f"Syntax Error in JSON: {e}")

# Entry/Proceed logic
if current_input_data:
    st.markdown("---")
    col_v, col_run = st.columns([1, 1])
    
    with col_v:
        st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
        if st.button("✨ Verify & Prepare Data", use_container_width=True):
            st.session_state.json_validated = True
            st.toast("Data structure verified!", icon="✅")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_run:
        if not st.session_state.json_validated:
            st.button("🚀 Analyze conversations", disabled=True, help="Verify data first", use_container_width=True)
        else:
            if st.button("🚀 Start Insights Engine", use_container_width=True):
                if not api_key:
                    st.error("System Error: API credentials not found in environment.")
                else:
                    ph = st.empty()
                    with ph.container():
                        st.markdown("<div class='custom-card' style='border-color:#3b82f6;'>", unsafe_allow_html=True)
                        st.info("⚙️ **Engine Initialized.** Starting deep analysis...")
                        p_bar = st.progress(0)
                        
                        try:
                            # Step 1: Identification
                            p_bar.progress(20)
                            emails_json = json.dumps(current_input_data)
                            threads = identify_threads(emails_json, api_key, model, verbose=True)
                            
                            if threads and "threads" in threads:
                                # Step 2: Analysis
                                thread_count = len(threads["threads"])
                                p_bar.progress(60)
                                analysis = analyze_threads(json.dumps(threads), api_key, model, verbose=True)
                                
                                if analysis and "analyzed_threads" in analysis:
                                    p_bar.progress(90)
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
                                    
                                    st.session_state.df_result = pd.DataFrame(df_rows)
                                    p_bar.progress(100)
                                    ph.empty()
                                    st.toast("Intelligence gathering complete!", icon="🎯")
                                else:
                                    st.error("Analysis Engine returned an empty result.")
                            else:
                                st.error("Thread Identification failed. Check data format.")
                        except Exception as e:
                            st.error(f"Processing Error: {e}")
                    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Input hash check (reset on change)
input_hash = hash(str(current_input_data)) if current_input_data else None
if input_hash != st.session_state.last_input_hash:
    st.session_state.json_validated = False
    st.session_state.last_input_hash = input_hash
    st.session_state.df_result = None

# Results Dashboard
if st.session_state.df_result is not None:
    df = st.session_state.df_result
    st.markdown("### 📊 Executive Overview")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total threads", len(df))
    with m2:
        high_risk = len(df[df['risk_level'].str.lower().str.contains('high|critical')])
        st.metric("Risk alerts", high_risk, delta="CRITICAL" if high_risk > 0 else None, delta_color="inverse")
    with m3:
        avg_sent = df['overall_sentiment'].mode()[0] if not df.empty else "N/A"
        st.metric("Core sentiment", avg_sent.capitalize())
        
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("#### 🔍 Thread Details")
    st.dataframe(df, width='stretch', hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    csv_bytes = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Analysis to CSV",
        data=csv_bytes,
        file_name="sales_report.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Footer if no data
if not current_input_data:
    st.markdown("""
    <div style='text-align: center; color: #94a3b8; padding: 4rem 1rem;'>
        <p style='font-size: 1.1rem;'>Awaiting data stream... Provide a JSON source above to start analysis.</p>
    </div>
    """, unsafe_allow_html=True)
