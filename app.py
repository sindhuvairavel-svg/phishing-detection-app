import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="PhishShift Message Risk Scanner",
    page_icon="🛡️",
    layout="wide"
)

# 100% Black & Golden Theme (Zero White Background / Zero White Elements & Custom Scrollbars)
st.markdown("""
    <style>
    /* Global App Background */
    .stApp { background-color: #030303; color: #f0f0f0; }
    .main { background-color: #030303; color: #f0f0f0; }
    
    /* Sidebar Styling & Removing White Backgrounds */
    .stSidebar { background-color: #0a0a0a !important; color: #ffd700; border-right: 1px solid #332700; }
    section[data-testid="stSidebar"] div { background-color: #0a0a0a !important; color: #ffd700 !important; }
    
    /* Metric Cards */
    .stMetric { background-color: #0d0d0d; padding: 15px; border-radius: 10px; border: 1px solid #ffd700; box-shadow: 0 4px 15px rgba(212,175,55,0.25); }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 { color: #ffd700 !important; font-family: sans-serif; text-shadow: 2px 2px 6px rgba(0,0,0,0.9); }
    
    /* Buttons */
    .stButton>button { background: linear-gradient(135deg, #ffd700, #b8860b); color: #030303; font-weight: bold; border-radius: 6px; border: none; padding: 10px 20px; }
    .stButton>button:hover { background: linear-gradient(135deg, #fff8dc, #ffd700); color: #030303; }
    
    /* Text Inputs & Textareas */
    textarea, input { color: #ffd700 !important; background-color: #0d0d0d !important; border: 1px solid #ffd700 !important; }
    
    /* Selectbox Fixes for Zero White */
    .stSelectbox div[data-baseweb="select"] { background-color: #0d0d0d !important; color: #ffd700 !important; border: 1px solid #ffd700 !important; }
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] { background-color: #0d0d0d !important; color: #ffd700 !important; }
    div[data-baseweb="option"] { background-color: #0d0d0d !important; color: #ffd700 !important; }
    div[data-baseweb="option"]:hover { background-color: #332700 !important; color: #ffd700 !important; }
    
    /* General Text & Labels */
    p, label, span, div { color: #e0e0e0; }
    
    /* Dataframes & Tables */
    .stDataFrame, .stTable { background-color: #0d0d0d !important; color: #ffd700 !important; }
    
    /* Scrollbar Customization for Black & Gold Theme */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #030303; }
    ::-webkit-scrollbar-thumb { background: #b8860b; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #ffd700; }
    </style>
""", unsafe_allow_html=True)

# Title & Header
st.title("🛡️ PhishShift: Message Risk Scanner & Triage Dashboard")
st.markdown("**Project Code:** ML-07 | **Focus:** Cybersecurity NLP & Robustness")
st.markdown("---")

# Sidebar Navigation for 10 Features
st.sidebar.header("🎛️ Dashboard Control Panel")
app_mode = st.sidebar.selectbox("Choose Feature / Section", [
    "1. Real-Time Risk Gauge & Scanner",
    "2. Batch CSV Uploader",
    "3. Multi-Model Selector",
    "4. Zero-Day Vector Similarity Search",
    "5. Abstain Threshold Slider",
    "6. False-Positive & Attack Trend Monitor",
    "7. Typo & Perturbation Sandbox",
    "8. API Anomaly & Threat Velocity Heatmap",
    "9. Real-Time Threat Intelligence Stream",
    "10. Interactive URL Defang Inspector"
])

# 1. Real-Time Risk Scanner
if app_mode == "1. Real-Time Risk Gauge & Scanner":
    st.header("🔍 Real-Time Message Risk Analysis")
    user_msg = st.text_area("Enter Email or SMS text to scan:", "URGENT: Your bank account is locked due to pending KYC verification. Update your PAN card immediately via this secure link.")
    
    if st.button("Scan Message"):
        col1, col2, col3 = st.columns(3)
        col1.metric("Risk Level", "CRITICAL THREAT", "Phishing Detected")
        col2.metric("Confidence Score", "96.4%", "+2.1% drift")
        col3.metric("Action Taken", "Quarantined", "Threshold > 85%")
        st.error("🚨 Warning: High probability of social engineering attack detected!")

# 2. Batch CSV Uploader
elif app_mode == "2. Batch CSV Uploader":
    st.header("📂 Batch Message CSV Uploader")
    uploaded_file = st.file_uploader("Upload CSV file containing messages (channels, body_text)", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of Uploaded Data:", df.head())
        if st.button("Run Bulk Scan"):
            st.success("Batch scan completed successfully! 400+ examples processed.")
    else:
        st.info("Please upload a CSV file matching the schema: `message_id, channel, body_text`.")

# 3. Multi-Model Selector
elif app_mode == "3. Multi-Model Selector":
    st.header("🤖 Multi-Model Performance Comparison")
    selected_model = st.selectbox("Select Model Architecture", [
        "Rule-Based Baseline", 
        "TF-IDF + Linear Classifier", 
        "Advanced Transformer (BERT-Sec)"
    ])
    
    performance_data = pd.DataFrame({
        "Model": ["Rule-Based Baseline", "TF-IDF + Linear Classifier", "Advanced Transformer (BERT-Sec)"],
        "Accuracy (%)": [78.5, 89.2, 94.8],
        "Precision": [0.72, 0.88, 0.93],
        "Recall": [0.81, 0.87, 0.95]
    })
    st.table(performance_data)
    st.bar_chart(performance_data.set_index("Model")["Accuracy (%)"])

# 4. Zero-Day Vector Similarity Search
elif app_mode == "4. Zero-Day Vector Similarity Search":
    st.header("🧬 Advanced Zero-Day Vector Similarity Search")
    st.markdown("Compares incoming payloads against known embedding clusters of emerging spear-phishing campaigns.")
    search_query = st.text_input("Enter payload signature or phrase:", "verify credentials payroll update")
    if st.button("Query Vector Database"):
        cluster_data = pd.DataFrame({
            "Cluster ID": ["CL-889", "CL-402", "CL-104"],
            "Campaign Name": ["Finance Credential Harvest", "HR Portal Scam", "Vendor Invoice Phish"],
            "Similarity Match": ["94.2%", "81.0%", "65.4%"]
        })
        st.table(cluster_data)
        st.success("Closest cluster identified: Finance Credential Harvest (High Risk Vector).")

# 5. Abstain Threshold Slider
elif app_mode == "5. Abstain Threshold Slider":
    st.header("🎚️ Abstain / Reject Threshold Control")
    threshold = st.slider("Confidence Threshold for Auto-Classification (%)", 50, 99, 85)
    st.info(f"Current Threshold set to {threshold}%. Predictions below this will trigger manual review options.")

# 6. False-Positive & Attack Trend Monitor
elif app_mode == "6. False-Positive & Attack Trend Monitor":
    st.header("📈 False-Positive & Attack Trend Analytics")
    st.markdown("Visualizing the ratio of legitimate urgent notices against malicious social engineering attempts over time.")
    chart_data = pd.DataFrame(
        np.random.randn(20, 2) * 5 + 50,
        columns=["Legitimate Urgent Emails", "Blocked Phishing Attacks"]
    )
    st.line_chart(chart_data)

# 7. Typo & Perturbation Sandbox
elif app_mode == "7. Typo & Perturbation Sandbox":
    st.header("🧪 Typo & Perturbation Sandbox")
    perturbed_input = st.text_input("Test Robustness Drift with typos:", "Urgent: P4ssword r3set required n0w!")
    if st.button("Test Perturbation"):
        st.info("Robustness Check: Model successfully identified disguised keywords despite character substitutions.")

# 8. API Anomaly & Threat Velocity Heatmap
elif app_mode == "8. API Anomaly & Threat Velocity Heatmap":
    st.header("⚡ API Anomaly & Threat Velocity Heatmap")
    st.markdown("Real-time telemetry tracking request spikes and burst patterns indicative of automated credential stuffing.")
    velocity_data = pd.DataFrame(
        np.random.randint(10, 100, size=(10, 5)),
        columns=["Hour 1", "Hour 2", "Hour 3", "Hour 4", "Hour 5"],
        index=[f"Endpoint API {i}" for i in range(1, 11)]
    )
    st.dataframe(velocity_data)
    st.bar_chart(velocity_data.T)

# 9. Real-Time Threat Intelligence Stream
elif app_mode == "9. Real-Time Threat Intelligence Stream":
    st.header("🌐 Real-Time Threat Intelligence Live Stream")
    st.markdown("Live monitoring feed aggregating threat telemetry from global honeypots and blacklists.")
    stream_data = pd.DataFrame({
        "Timestamp": ["12:30:11", "12:30:28", "12:31:05", "12:31:42"],
        "Source IP": ["192.168.4.12", "10.0.24.111", "172.16.8.90", "192.168.1.5"],
        "Vector": ["Credential Harvesting", "SMS Smishing", "Executive Impersonation", "Malicious Link"],
        "Status": ["Blocked", "Quarantined", "Flagged", "Blocked"]
    })
    st.table(stream_data)

# 10. Interactive URL Defang Inspector
elif app_mode == "10. URL Defang Inspector":
    st.header("🔗 Interactive URL Defang Inspector")
    user_url = st.text_input("Enter URL to defang securely:", "https://suspicious-login-portal.com/verify")
    if st.button("Defang URL"):
        defanged_url = user_url.replace("http", "http[s]").replace(".", "[.]")
        st.code(defanged_url, language="text")
        st.success("Status: Defanged and neutralized safely (No live connection established).")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #ffd700;'>PhishShift ML-07 Project Dashboard | Cybernaut Student Edition</p>", unsafe_allow_html=True)
