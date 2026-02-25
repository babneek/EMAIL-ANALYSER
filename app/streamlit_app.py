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
    /* Gradient Background for Header */
    .main {
        background: #f8f9fa;
    }
    .stTitle {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
    }
    .stSubheader {
        color: #4b5563;
        font-weight: 400;
    }
    
    /* Card Styling */
    .css-1r6p8d1 { 
        background-color: white; 
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        padding: 2rem;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.5);
    }
    
    /* Metric Card Styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #1e40af;
    }
    
    /* Hide Deploy button */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/analytics.png", width=64)
    st.title("SimplAI Email")
    
    st.markdown("### System Status")
    api_key_status = "✅ Configured" if os.getenv("OPENAI_API_KEY") else "❌ Missing API Key"
    st.write(f"API Key: {api_key_status}")
    
    model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
    st.write(f"Active Model: `{model_name}`")
    
    st.markdown("---")
    
    # Hidden Configuration (in expander)
    with st.sidebar.expander("⚙️ Advanced Settings"):
        api_key = st.text_input("Override OpenAI API Key", value=os.getenv("OPENAI_API_KEY", ""), type="password")
        
        # Get model list and default
        env_model = os.getenv("MODEL_NAME", "gpt-4o-mini")
        model_options = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
        if env_model not in model_options:
            model_options.insert(0, env_model)
        
        model = st.selectbox("LLM Model", model_options, index=model_options.index(env_model) if env_model in model_options else 0)
    
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY", "")
    if not model:
        model = os.getenv("MODEL_NAME", "gpt-4o-mini")

    st.markdown("### Instructions")
    st.info("1. Provide email data via upload or paste\n2. Click 'Run Analytics'\n3. Download the generated CSV report")

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Email Thread Analytics")
    st.subheader("Transform unstructured sales conversations into actionable data insights.")

# Input Section
st.markdown("### 📥 Input Data")
tab1, tab2 = st.tabs(["📄 Upload JSON File", "✍️ Paste JSON Text"])

# Initialize session state for validation
if 'json_validated' not in st.session_state:
    st.session_state.json_validated = False
if 'last_input_hash' not in st.session_state:
    st.session_state.last_input_hash = None

emails_data = None
current_input_data = None

with tab1:
    uploaded_file = st.file_uploader("Choose a JSON file...", type=["json"])
    if uploaded_file:
        try:
            content = uploaded_file.read().decode("utf-8")
            current_input_data = json.loads(content)
            if st.button("🔍 Check & Validate File"):
                st.session_state.json_validated = True
                st.success("JSON File is valid and ready for processing!")
        except Exception as e:
            st.error(f"Error reading file: {e}")
            st.session_state.json_validated = False

with tab2:
    json_text = st.text_area("Paste JSON here...", height=200, help="Paste the content of your sales emails JSON.")
    if json_text:
        try:
            current_input_data = json.loads(json_text)
            if st.button("✔️ Check & Validate Text"):
                st.session_state.json_validated = True
                st.success("JSON Text is valid! You can now proceed to run analytics.")
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON format: {e}")
            st.session_state.json_validated = False

# Reset validation if input changes (simple hash check)
input_hash = hash(str(current_input_data)) if current_input_data else None
if input_hash != st.session_state.last_input_hash:
    st.session_state.json_validated = False
    st.session_state.last_input_hash = input_hash

# Process Section
if current_input_data:
    emails_data = current_input_data
    
    # Display Preview
    with st.expander("🔍 Preview Input Data"):
        st.json(emails_data)
        
    if not st.session_state.json_validated:
        st.warning("Please click the 'Check & Validate' button above before proceeding.")
        
    if st.button("🚀 Run Analytics", disabled=not st.session_state.json_validated):
        if not api_key:
            st.error("OpenAI API Key is missing. Please set it in .env or Advanced Settings.")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Identification
                status_text.text("Step 1/3: Identifying email threads...")
                progress_bar.progress(10)
                
                emails_json = json.dumps(emails_data)
                threads = identify_threads(emails_json, api_key, model, verbose=True)
                
                if threads and "threads" in threads:
                    thread_count = len(threads["threads"])
                    status_text.text(f"Found {thread_count} threads. Step 2/3: Analyzing sentiment and risks...")
                    progress_bar.progress(40)
                    
                    # Step 2: Analysis
                    analysis = analyze_threads(json.dumps(threads), api_key, model, verbose=True)
                    
                    if analysis and "analyzed_threads" in analysis:
                        status_text.text("Step 3/3: Generating CSV report...")
                        progress_bar.progress(80)
                        
                        # Step 3: Export to Dataframe & CSV
                        df_rows = []
                        fieldnames = [
                            'thread_id', 'conversation_id', 'thread_topic', 'email_count', 
                            'participants', 'overall_sentiment', 'sentiment_trend', 
                            'client_requirements', 'open_questions', 'sales_rep_understanding', 
                            'sales_rep_gaps', 'risk_level', 'recommended_next_action', 'last_updated'
                        ]
                        
                        for thread in analysis["analyzed_threads"]:
                            row = {}
                            for field in fieldnames:
                                val = thread.get(field, '')
                                if isinstance(val, list):
                                    row[field] = "; ".join(map(str, val))
                                else:
                                    row[field] = val
                            df_rows.append(row)
                        
                        df = pd.DataFrame(df_rows)
                        
                        # Clear progress
                        progress_bar.progress(100)
                        status_text.success("Analysis Complete!")
                        
                        # Display Metrics
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Total Threads", thread_count)
                        high_risk = len(df[df['risk_level'].str.lower() == 'high'])
                        m2.metric("High Risk Threads", high_risk, delta=None if high_risk == 0 else "-!")
                        avg_sentiment = df['overall_sentiment'].mode()[0] if not df.empty else "N/A"
                        m3.metric("Primary Sentiment", avg_sentiment.capitalize())
                        
                        # Display Dataframe
                        st.subheader("📊 Analysis Results")
                        st.dataframe(df, use_container_width=True)
                        
                        # Download Link
                        csv_data = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Analytics CSV",
                            data=csv_data,
                            file_name="email_thread_analytics.csv",
                            mime="text/csv",
                        )
                    else:
                        st.error("Failed to analyze threads. Please check your data format.")
                else:
                    st.error("Failed to identify threads. Please check your data format.")
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")

else:
    # Welcome View
    st.markdown("""
    ---
    ### How it works
    This application uses **gpt-4o-mini** to:
    - **🧵 Thread Discovery**: Group long email chains into specific topical threads (e.g., Pricing vs Implementation).
    - **📊 Sentiment Tracking**: Monitor if the relationship is improving or declining.
    - **📋 Requirement Extraction**: Capture what the client actually wants.
    - **🛡️ Risk Assessment**: Identify potential deal-breakers before they happen.
    
    Choose an input method above to get started. You can use `sample_emails.json` as a test file.
    """)
    
    # Show example structure
    with st.expander("📋 Example JSON Structure"):
        st.code("""
{
  "conversations": [
    {
      "conversation_id": "CONV_001",
      "emails": [
        {
          "email_id": "E001",
          "sender": "client@example.com",
          "recipient": "sales@company.com",
          "timestamp": "2024-02-25T10:00:00Z",
          "subject": "Pricing inquiry",
          "body": "How much for 100 users?"
        }
      ]
    }
  ]
}
        """, language="json")
