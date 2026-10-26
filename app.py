import time
import random
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Phishing Detection Project - AI Security",
    page_icon="🛡️",
    layout="wide",
)

# Custom CSS for Dark Theme Dashboard styling matching the image
st.markdown(
    """
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    .stSidebar { background-color: #161b22; }
    div.stButton > button { background-color: #f1c40f; color: #000000; font-weight: bold; border-radius: 5px; }
    .metric-card { background-color: #1f242d; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar Navigation
st.sidebar.image(
    "https://img.icons8.com/color/96/shield.png", width=60
)  # Placeholder logo
st.sidebar.markdown(
    "### **Smarter Detection**\nSafer Tomorrow[span_6](start_span)[span_6](end_span)"
)
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🔍 Risk Scanner",
        "📊 Model Analysis",
        "🌐 Threat Intelligence",
        "⚙️ Settings",
    ],
)

# Top Bar Header
col_title, col_status = st.columns([3, 1])
with col_title:
    st.markdown(
        "## 🛡️ Phishing Detection Project\n**AI-Powered Email & SMS Security**[span_7](start_span)[span_7](end_span)"
    )
with col_status:
    st.markdown(
        "🟢 **System Online**  \n📅 Apr 26, 2025 | 10:42 AM[span_8](start_span)[span_8](end_span)",
        unsafe_allow_html=True,
    )

st.markdown("---")

# ==================== HOME & QUICK SCAN TAB ====================
if menu == "🏠 Home" or menu == "🔍 Risk Scanner":

  row1_col1, row1_col2, row1_col3 = st.columns([1.2, 1.2, 1.1])

  # Quick Scan Section
  with row1_col1:
    st.markdown("### ⚡ Quick Scan")
    st.markdown(
        "<p style='font-size:12px; color:gray;'>Check if a message is phishing or safe[span_9](start_span)[span_9](end_span)</p>",
        unsafe_allow_html=True,
    )

    scan_type = st.radio(
        "Type", ["Email", "SMS"], horizontal=True, label_visibility="collapsed"
    )
    user_input = st.text_area(
        "Enter content",
        placeholder="e.g., https://example.com/verify-account[span_10](start_span)[span_10](end_span)",
        height=100,
    )

    if st.button("Scan"):
      if user_input:
        with st.spinner("Analyzing message with AI models..."):
          time.sleep(1)
        st.session_state["scanned"] = True
        st.session_state["input_text"] = user_input
      else:
        st.warning("Please enter some text to scan.")

  # Detection Result Section
  with row1_col2:
    st.markdown("### 🎯 Detection Result")
    if st.session_state.get("scanned", False):
      st.markdown(
          "<h3 style='color: #ff4d4d;'>⚠️ Phishing</h3>", unsafe_allow_html=True
      )
      st.markdown("**Risk Score:** <span style='color:red;'>82.6%</span>", unsafe_allow_html=True) #[span_11](start_span)[span_11](end_span)
      st.markdown("**Confidence:** 91.2%[span_12](start_span)[span_12](end_span)")
      st.markdown("**Model:** Random Forest[span_13](start_span)[span_13](end_span)")
      st.markdown(
          "**Threat Level:** <span style='color:red;'>High</span>",
          unsafe_allow_html=True,
      )
      st.error(
          "🚨 Do not click. This looks suspicious."
      )  #[span_14](start_span)[span_14](end_span)
    else:
      st.info(
          "Perform a Quick Scan to view the risk score and classification"
          " results."
      )

  # Model Performance Summary
  with row1_col3:
    st.markdown("### 📈 Model Performance")
    st.selectbox(
        "Select Model", ["Random Forest", "SVM", "Logistic Regression", "Naive Bayes"], label_visibility="collapsed"
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Accuracy", "94.2%")  #[span_15](start_span)[span_15](end_span)
    m2.metric("Precision", "92.2%")  #[span_16](start_span)[span_16](end_span)
    m3.metric("Recall", "88.8%")  #[span_17](start_span)[span_17](end_span)
    m4.metric("F1-Score", "90.5%")  #[span_18](start_span)[span_18](end_span)

  st.markdown("---")

  # Row 2: XAI & Advanced Security
  row2_col1, row2_col2, row2_col3 = st.columns([1.2, 1.2, 1.1])

  with row2_col1:
    st.markdown("### 🔍 Explainable AI (XAI)")
    st.markdown(
        "<p style='font-size:12px; color:gray;'>Why this message is flagged?[span_19](start_span)[span_19](end_span)</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "> *Congratulations! You have won a free gift. Click here to claim"
        " now: <span style='color:red;'>https://bit.ly/7x1z</span>*[span_20](start_span)[span_20](end_span)",
        unsafe_allow_html=True,
    )

    st.markdown("**Key Factors:**[span_21](start_span)[span_21](end_span)")
    st.progress(0.38, text="Suspicious URL (0.38)[span_22](start_span)[span_22](end_span)")
    st.progress(0.24, text="Urgent Language (0.24)[span_23](start_span)[span_23](end_span)")
    st.progress(0.18, text="Free Gift / Reward (0.18)[span_24](start_span)[span_24](end_span)")
    st.progress(0.12, text="Shortened Domain (0.12)[span_25](start_span)[span_25](end_span)")

  with row2_col2:
    st.markdown("### 📊 False Detection Monitor")
    st.markdown(
        "<p style='font-size:12px; color:gray;'>Track model mistakes and reduce"
        " them[span_26](start_span)[span_26](end_span)</p>",
        unsafe_allow_html=True,
    )
    f_col1, f_col2 = st.columns(2)
    f_col1.metric("False Positives", "12 (1.8%)")  #[span_27](start_span)[span_27](end_span)
    f_col2.metric("False Negatives", "7 (1.1%)")  #[span_28](start_span)[span_28](end_span)

    # Error Rate trend chart placeholder
    chart_data = pd.DataFrame(
        {
            "False Positives": [3, 4, 3, 5, 4, 3],
            "False Negatives": [2, 1, 2, 1, 2, 1],
        },
        index=["Apr 20", "Apr 21", "Apr 22", "Apr 23", "Apr 24", "Apr 25"],
    )  #[span_29](start_span)[span_29](end_span)
    st.line_chart(chart_data, height=150)

  with row2_col3:
    st.markdown("### 🛡️ Advanced Security")
    st.markdown(
        "<p style='font-size:12px; color:gray;'>Extra protection layers</p>",
        unsafe_allow_html=True,
    )
    st.toggle("Threat Intelligence", value=True)  #[span_30](start_span)[span_30](end_span)
    st.toggle("URL Reputation Check", value=True)  #[span_31](start_span)[span_31](end_span)
    st.toggle("IP Reputation Check", value=True)  #[span_32](start_span)[span_32](end_span)
    st.toggle("Malicious Domain Detection", value=True)  #[span_33](start_span)[span_33](end_span)
    st.toggle("Behaviour Analysis", value=True)  #[span_34](start_span)[span_34](end_span)

# ==================== MODEL ANALYSIS TAB ====================
elif menu == "📊 Model Analysis":
  st.markdown("### 📊 Comprehensive Model Analysis")
  st.markdown(
      "Compare accuracy across different machine learning models used for"
      " phishing detection."
  )

  perf_df = pd.DataFrame(
      {
          "Model": [
              "Random Forest",
              "SVM",
              "Logistic Regression",
              "Naive Bayes",
          ],
          "Accuracy (%)": [94.2, 89.1, 86.7, 82.3],  #[span_35](start_span)[span_35](end_span)
      }
  )
  st.bar_chart(perf_df.set_index("Model"))

  st.markdown("### 🎛️ Threshold Optimizer")
  threshold = st.slider("Select Threshold", 50, 99, 72)  #[span_36](start_span)[span_36](end_span)
  st.write(f"Current Optimized Threshold: {threshold}%")

# ==================== THREAT INTELLIGENCE TAB ====================
elif menu == "🌐 Threat Intelligence":
  st.markdown("### 🌐 Real-Time Threat Intelligence & Global Attack Map")
  st.markdown(
      "Live threat data tracking malicious domains, phishing URLs, and C2"
      " servers[span_37](start_span)[span_37](end_span)."
  )

  t1, t2, t3, t4 = st.columns(4)
  t1.metric("Malicious Domains", "124")  #[span_38](start_span)[span_38](end_span)
  t2.metric("Phishing URLs", "342")  #[span_39](start_span)[span_39](end_span)
  t3.metric("C2 Servers", "67")  #[span_40](start_span)[span_40](end_span)
  t4.metric("Suspicious IPs", "218")  #[span_41](start_span)[span_41](end_span)

  st.map(
      pd.DataFrame(
          {
              "lat": [37.7749, 51.5074, 35.6762, 28.6139],
              "lon": [-122.4194, -0.1278, 139.6503, 77.2090],
          }
      )
  )

# ==================== SETTINGS TAB ====================
elif menu == "⚙️ Settings":
  st.markdown("### ⚙️ System Settings")
  st.text_input("API Key Configuration", "sk-ant-api03-xxxxxxxx")
  st.number_input("Batch Scan Limit (Max Rows)", 100, 1000, 500)  #[span_42](start_span)[span_42](end_span)
  st.checkbox("Enable Real-Time Alerts", value=True)
  if st.button("Save Settings"):
    st.success("Settings saved successfully!")
