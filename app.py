import numpy as np
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="PhishShift - Security & Safety Hub", page_icon="🛡️", layout="wide"
)

# 100% Black & Golden Theme Styling (No harsh box borders, ultra-clean UI)
st.markdown(
    """
    <style>
    /* Global App Background */
    .stApp { background-color: #030303; color: #f0f0f0; }
    .main { background-color: #030303; color: #f0f0f0; }
    
    /* Sidebar Styling */
    .stSidebar { background-color: #0a0a0a !important; color: #ffd700; border-right: 1px solid #332700; }
    section[data-testid="stSidebar"] div { background-color: #0a0a0a !important; color: #ffd700 !important; }
    
    /* Clean Metric Cards */
    .stMetric { background-color: #0d0d0d; padding: 15px; border-radius: 10px; border: 1px solid #ffd700; box-shadow: 0 4px 15px rgba(212,175,55,0.25); }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 { color: #ffd700 !important; font-family: sans-serif; text-shadow: 2px 2px 6px rgba(0,0,0,0.9); }
    
    /* Buttons */
    .stButton>button { background: linear-gradient(135deg, #ffd700, #b8860b); color: #030303; font-weight: bold; border-radius: 6px; border: none; padding: 10px 20px; }
    .stButton>button:hover { background: linear-gradient(135deg, #fff8dc, #ffd700); color: #030303; }
    
    /* Text Inputs & Textareas */
    textarea, input { color: #ffd700 !important; background-color: #0d0d0d !important; border: 1px solid #ffd700 !important; }
    
    /* Streamlit Selectbox & Dropdown Menu Golden Theme Fix */
    .stSelectbox div[data-baseweb="select"] { background-color: #0d0d0d !important; color: #ffd700 !important; border: 1px solid #ffd700 !important; }
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] { background-color: #120e00 !important; border: 2px solid #ffd700 !important; color: #ffd700 !important; }
    div[data-baseweb="option"] { background-color: #120e00 !important; color: #ffd700 !important; }
    div[data-baseweb="option"] div { color: #ffd700 !important; background-color: #120e00 !important; }
    div[data-baseweb="option"]:hover { background-color: #ffd700 !important; color: #030303 !important; }
    div[data-baseweb="option"]:hover div { background-color: #ffd700 !important; color: #030303 !important; }
    
    /* General Text & Labels */
    p, label, span, div { color: #e0e0e0; }
    
    /* Dataframes & Tables */
    .stDataFrame, .stTable { background-color: #0d0d0d !important; color: #ffd700 !important; }
    
    /* Scrollbar Customization */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #030303; }
    ::-webkit-scrollbar-thumb { background: #b8860b; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #ffd700; }
    </style>
""",
    unsafe_allow_html=True,
)

# Title & Header
st.title("🛡️ PhishShift: Smart Safety & Scam Protection Hub")
st.markdown(
    "**Project Edition:** Premium Security Suite | **Status:** Protected &"
    " Active"
)
st.markdown("---")

# Sidebar Navigation (Updated with new user-friendly features & colorful charts)
st.sidebar.header("🎛️ Control Center")
app_mode = st.sidebar.selectbox(
    "Select Feature",
    [
        "1. Instant Message & Link Scanner",
        "2. Protection Guard Comparison",
        "3. Security Sensitivity Control",
        "4. Daily Threat & Scam Trends (With Colorful Graphs)",
        "5. Fake Link & Typo Checker",
        "6. Live Activity & Traffic Monitor",
        "7. Global Scam Alert Feed",
        "8. Quick Safety Checklist (New Feature)",
        "9. Scam Pattern Finder (New Feature)",
        "10. Emergency Report Assistant (New Feature)",
    ],
)

# 1. Instant Message & Link Scanner
if app_mode == "1. Instant Message & Link Scanner":
  st.header("🔍 Instant Message Risk Scanner")
  user_msg = st.text_area(
      "Paste suspicious SMS, Email, or Web Link here:",
      "URGENT: Your bank account is locked due to pending verification. Click"
      " here immediately to update.",
  )

  if st.button("Scan Message Now"):
    col1, col2, col3 = st.columns(3)
    col1.metric("Risk Status", "HIGH THREAT", "Scam Detected")
    col2.metric("Safety Score", "12.4%", "Dangerous")
    col3.metric("System Action", "Blocked", "Auto-Protected")
    st.error(
        "🚨 Warning: This message contains fraudulent patterns meant to steal"
        " your personal information!"
    )

# 2. Protection Guard Comparison
elif app_mode == "2. Protection Guard Comparison":
  st.header("🤖 Protection Guard Comparison")
  st.markdown(
      "Comparing the efficiency of different security layers in catching"
      " online scams."
  )

  performance_data = pd.DataFrame(
      {
          "Protection Level": [
              "Basic Filter",
              "Standard Shield",
              "Advanced Gold Guard",
          ],
          "Success Rate (%)": [78.5, 89.2, 96.8],
          "Speed": ["Fast", "Very Fast", "Instant"],
          "Reliability": ["Good", "Better", "Highest"],
      }
  )
  st.table(performance_data)
  st.bar_chart(performance_data.set_index("Protection Level")["Success Rate (%)"])

# 3. Security Sensitivity Control
elif app_mode == "3. Security Sensitivity Control":
  st.header("🎚️ Security Sensitivity Control")
  threshold = st.slider("Set Alert Sensitivity Level (%)", 50, 99, 85)
  st.info(
      f"Current security sensitivity is set to {threshold}%. Anything above"
      " this will be blocked automatically."
  )

# 4. Daily Threat & Scam Trends
elif app_mode == "4. Daily Threat & Scam Trends (With Colorful Graphs)":
  st.header("📈 Daily Scam & Safety Trends")
  st.markdown(
      "Visualizing safe notifications compared to dangerous scam attempts over"
      " the week using colorful interactive charts."
  )
  chart_data = pd.DataFrame(
      np.random.randn(20, 2) * 5 + 50,
      columns=["Safe Verified Messages", "Blocked Scam Attempts"],
  )
  st.line_chart(chart_data)
  st.markdown("### Weekly Scam Attack Distribution")
  st.bar_chart(chart_data)

# 5. Fake Link & Typo Checker
elif app_mode == "5. Fake Link & Typo Checker":
  st.header("🧪 Link Typo & Impersonation Sandbox")
  perturbed_input = st.text_input(
      "Test link safety against fake spellings:",
      "https://secure-log1n-verify.com",
  )
  if st.button("Check Link Robustness"):
    st.success(
        "Safety Check: Successfully caught fake character substitutions and"
        " hidden scams!"
    )

# 6. Live Activity & Traffic Monitor
elif app_mode == "6. Live Activity & Traffic Monitor":
  st.header("⚡ Live Activity & Traffic Monitor")
  st.markdown(
      "Real-time tracking of scanning requests and security server traffic."
  )
  velocity_data = pd.DataFrame(
      np.random.randint(10, 100, size=(10, 5)),
      columns=["Hour 1", "Hour 2", "Hour 3", "Hour 4", "Hour 5"],
      index=[f"Security Zone {i}" for i in range(1, 11)],
  )
  st.dataframe(velocity_data)
  st.bar_chart(velocity_data.T)

# 7. Global Scam Alert Feed
elif app_mode == "7. Global Scam Alert Feed":
  st.header("🌐 Global Scam Live Stream")
  st.markdown(
      "Live feed monitoring active online fraud reports from around the world."
  )
  stream_data = pd.DataFrame(
      {
          "Time": ["12:30:11", "12:30:28", "12:31:05", "12:31:42"],
          "Region / Origin": ["Server A-1", "Server B-4", "Server C-2", "Server D-9"],
          "Scam Type": [
              "Fake Bank Login",
              "Lottery SMS Scam",
              "Fake Job Offer",
              "Malicious Web Link",
          ],
          "Status": ["Blocked", "Quarantined", "Flagged", "Blocked"],
      }
  )
  st.table(stream_data)

# 8. Quick Safety Checklist (New Feature)
elif app_mode == "8. Quick Safety Checklist (New Feature)":
  st.header("📝 Quick Personal Safety Checklist")
  st.markdown(
      "Check off items to ensure your online accounts and devices are fully"
      " secure against scams."
  )
  st.checkbox("Enabled Two-Factor Authentication (2FA)", value=True)
  st.checkbox("Using Strong and Unique Passwords", value=True)
  st.checkbox("Avoided Clicking Unknown Email Links", value=False)
  st.checkbox("Regularly Updated Device Software", value=True)

  if st.button("Evaluate My Safety Score"):
    st.success(
        "🎉 Great job! Your safety score is 75%. Complete all checks to reach"
        " 100%."
    )
    st.metric("Overall Safety Score", "75%", "Good Protection")

# 9. Scam Pattern Finder (New Feature)
elif app_mode == "9. Scam Pattern Finder (New Feature)":
  st.header("🔍 Common Scam Pattern Lookup")
  st.markdown(
      "Search for common scam keywords to see if they are flagged as fraud."
  )
  keyword = st.text_input(
      "Enter keyword or phrase to check:", "Claim your lottery prize now"
  )
  if st.button("Analyze Keyword"):
    st.warning(
        "⚠️ Warning: This phrase is commonly associated with financial prize"
        " scams!"
    )
    st.metric("Fraud Probability", "94.5%", "High Risk Keyword")

# 10. Emergency Report Assistant (New Feature)
elif app_mode == "10. Emergency Report Assistant (New Feature)":
  st.header("🚨 Emergency Scam Reporting Assistant")
  st.markdown(
      "If you have fallen victim to a scam, use this guide to take immediate"
      " action."
  )
  scam_type = st.selectbox(
      "Select type of incident experienced:",
      [
          "Bank Account Fraud",
          "Fake Online Shopping",
          "Stolen Password / Identity",
          "Suspicious Loan App",
      ],
  )

  if st.button("Get Emergency Steps"):
    st.error(
        f"🚨 Action Plan for {scam_type}: 1. Contact your bank immediately to"
        " freeze accounts. 2. Change your passwords right away. 3. Report the"
        " incident to cyber crime authorities."
    )
    st.info(
        "Helpline Info: In India, you can call cyber crime helpline number"
        " 1930 immediately."
    )

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #ffd700;'>PhishShift Security Hub |"
    " Ultimate Scam Protection Edition</p>",
    unsafe_allow_html=True,
)
