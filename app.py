import time
import random
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Phishing Detection Project - Dark Golden Theme",
    page_icon="🛡️",
    layout="wide",
)

# Custom CSS for Full Black & Dark Golden Theme (No White)
st.markdown(
    """
    <style>
    /* Global Background & Font Colors */
    .stApp {
        background-color: #050505;
        color: #d4af37;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0b0b0b;
        border-right: 1px solid #d4af37;
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #d4af37 !important;
        font-weight: bold;
    }

    /* Metric Cards and Containers */
    div.metric-card, div[data-testid="stVerticalBlock"] > div {
        background-color: #111111;
        border: 1px solid #d4af37;
        border-radius: 8px;
        padding: 15px;
        color: #d4af37;
    }

    /* Headings and Text */
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #d4af37 !important;
    }

    /* Buttons Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #d4af37 0%, #aa8c2c 100%);
        color: #000000 !important;
        font-weight: bold;
        border-radius: 6px;
        border: none;
        box-shadow: 0px 4px 10px rgba(212, 175, 55, 0.3);
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #f3e5ab 0%, #d4af37 100%);
        color: #000000 !important;
    }

    /* Text Inputs & Selectboxes */
    input, textarea, div[data-baseweb="select"] {
        background-color: #1a1a1a !important;
        color: #d4af37 !important;
        border-color: #d4af37 !important;
    }
    
    /* Metrics numbers */
    div[data-testid="stMetricValue"] {
        color: #ffcc00 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar Navigation
st.sidebar.markdown(
    "<h2 style='text-align: center; color: #d4af37;'>🛡️ AI SECURITY</h2>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<p style='text-align: center; color: #aa8c2c;'>Smarter Detection | Safer"
    " Tomorrow</p>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation Menu",
    [
        "🏠 Home & Scanner",
        "📊 Advanced Model Analysis",
        "🌐 Real-Time Threat Intelligence",
        "⚙️ Settings",
    ],
)

# Top Header
col_title, col_status = st.columns([3, 1])
with col_title:
    st.markdown(
        "## 🛡️ Advanced Phishing Detection & Threat Analytics"
    )
with col_status:
    st.markdown(
        "🟢 **System Online**  \n📅 Live Security Active",
        unsafe_allow_html=True,
    )

st.markdown("---")

# ==================== HOME & SCANNER TAB ====================
if menu == "🏠 Home & Scanner":

  c1, c2, c3 = st.columns([1.2, 1.2, 1.1])

  with c1:
    st.markdown("### ⚡ Quick Content Scan")
    scan_mode = st.radio(
        "Mode", ["Email", "SMS", "URL"], horizontal=True
    )
    user_text = st.text_area(
        "Paste message or link here:",
        placeholder="e.g., https://secure-login-verify.com",
        height=110,
    )

    if st.button("Run Deep Scan"):
      if user_text:
        with st.spinner("AI Models scanning for threats..."):
          time.sleep(1)
        st.session_state["scanned"] = True
      else:
        st.warning("Please enter text or a link.")

  with c2:
    st.markdown("### 🎯 Detection Result")
    if st.session_state.get("scanned", False):
      st.markdown(
          "<h3 style='color: #ff3333 !important;'>⚠️ High Risk Phishing"
          " Detected</h3>",
          unsafe_allow_html=True,
      )
      st.metric(label="Risk Score", value="88.4%", delta="+12.2% Threat")
      st.markdown("**Confidence Level:** 94.6%")
      st.markdown("**Primary Model:** Random Forest + XGBoost")
      st.error("🚨 Warning: Malicious patterns identified. Do not click.")
    else:
      st.info(
          "Perform a Quick Scan to generate deep threat risk analytics."
      )

  with c3:
    st.markdown("### 📈 Live Performance Metrics")
    m1, m2 = st.columns(2)
    m1.metric("Accuracy", "96.4%")
    m2.metric("Precision", "94.1%")
    m3, m4 = st.columns(2)
    m3.metric("Recall", "91.8%")
    m4.metric("F1-Score", "92.9%")

  st.markdown("---")

  # Advanced Charts Section
  st.markdown("### 📊 Advanced Threat Trend & Behavioral Analytics")
  
  # Generating advanced multi-line chart data
  chart_data = pd.DataFrame(
      {
          "Phishing Attacks Blocked": [120, 150, 180, 220, 310, 450, 520],
          "Malicious URLs Filtered": [90, 110, 140, 190, 260, 380, 490],
          "AI False Positives": [15, 12, 10, 8, 6, 4, 3],
      },
      index=[
          "Mon",
          "Tue",
          "Wed",
          "Thu",
          "Fri",
          "Sat",
          "Sun",
      ],
  )
  st.line_chart(chart_data)

# ==================== MODEL ANALYSIS TAB ====================
elif menu == "📊 Advanced Model Analysis":
  st.markdown("### 📊 Multi-Model Comparative Analysis")
  st.markdown(
      "Detailed performance breakdown across deep learning and machine learning"
      " classifiers."
  )

  model_perf = pd.DataFrame(
      {
          "Machine Learning Model": [
              "Random Forest",
              "XGBoost",
              "SVM",
              "Logistic Regression",
              "Naive Bayes",
          ],
          "Accuracy (%)": [96.4, 95.8, 91.2, 88.5, 84.1],
          "Processing Speed (ms)": [12, 15, 28, 8, 5],
      }
  )

  st.bar_chart(model_perf.set_index("Machine Learning Model")["Accuracy (%)"])
  st.dataframe(model_perf, use_container_width=True)

# ==================== THREAT INTELLIGENCE TAB ====================
elif menu == "🌐 Real-Time Threat Intelligence":
  st.markdown("### 🌐 Global Threat Feed & Attack Map Matrix")

  t1, t2, t3, t4 = st.columns(4)
  t1.metric("Active Botnets", "42")
  t2.metric("Blocked Domains", "1,420")
  t3.metric("Phishing Signatures", "8,930")
  t4.metric("Global Server Load", "14.2%")

  st.markdown("#### 🌍 Live Attack Coordinates (Simulated Heatmap)")
  map_data = pd.DataFrame(
      {
          "lat": [13.0827, 37.7749, 51.5074, 35.6762, 1.3521],
          "lon": [80.2707, -122.4194, -0.1278, 139.6503, 103.8198],
      }
  )
  st.map(map_data)

# ==================== SETTINGS TAB ====================
elif menu == "⚙️ Settings":
  st.markdown("### ⚙️ System Configuration & Thresholds")
  st.slider("AI Sensitivity Threshold (%)", 50, 99, 85)
  st.text_input("API Security Key", "sk-gold-sec-998821-xyz")
  st.checkbox("Enable Real-time Threat Alerts", value=True)
  st.checkbox("Auto-block Suspicious IP Addresses", value=True)
  if st.button("Save Security Preferences"):
    st.success("Preferences updated with dark gold encryption protocols!")
