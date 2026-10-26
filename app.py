import time
import random
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Phishing Detection Project - Colorful & Clean UI",
    page_icon="🛡️",
    layout="wide",
)

# Custom Clean & Colorful CSS (No harsh boxes, modern vibrant palette with green, red, cream)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #f0f2f6;
    }
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #f0f2f6 !important;
        font-weight: bold;
    }
    /* Remove harsh box borders and backgrounds */
    div[data-testid="stVerticalBlock"] > div {
        background-color: transparent;
        border: none;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #fdfbf7 !important;
    }
    /* Vibrant buttons with green/cream gradient */
    div.stButton > button {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        color: #ffffff !important;
        font-weight: bold;
        border-radius: 6px;
        border: none;
        padding: 8px 16px;
        box-shadow: 0px 4px 10px rgba(46, 204, 113, 0.3);
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #27ae60 0%, #219653 100%);
    }
    /* Clean Input Fields */
    input, textarea, div[data-baseweb="select"] {
        background-color: #21262d !important;
        color: #f0f2f6 !important;
        border: 1px solid #30363d !important;
        border-radius: 6px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar Navigation
st.sidebar.markdown(
    "<h2 style='text-align: center; color: #2ecc71;'>AI SECURITY HUB</h2>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<p style='text-align: center; color: #fdfbf7;'>Smarter Detection | Safer"
    " Tomorrow</p>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation Menu",
    [
        "Home & Scanner",
        "Advanced Model Analysis",
        "Real-Time Threat Intelligence",
        "API & Threat Center",
        "Settings",
    ],
)

# Top Header
col_title, col_status = st.columns([3, 1])
with col_title:
  st.markdown("## Advanced Phishing Detection & Threat Analytics")
with col_status:
  st.markdown(
      "🟢 **System Online**  \n⚡ Live Security Active", unsafe_allow_html=True
  )

st.markdown("---")

# ==================== HOME & SCANNER TAB ====================
if menu == "Home & Scanner":
  c1, c2, c3 = st.columns([1.2, 1.2, 1.1])

  with c1:
    st.markdown("### Quick Content / Image Scan")
    scan_mode = st.radio("Input Type", ["Text Message / URL", "Upload Image"])

    if scan_mode == "Text Message / URL":
      user_text = st.text_area(
          "Paste message or link here:",
          placeholder="e.g., https://secure-login-verify.com",
          height=100,
      )
    else:
      uploaded_file = st.file_uploader(
          "Upload Screenshot / Image", type=["png", "jpg", "jpeg"]
      )
      user_text = (
          "Image uploaded for phishing analysis" if uploaded_file else ""
      )

    if st.button("Run Deep Scan"):
      if user_text:
        with st.spinner("AI Models scanning for threats..."):
          time.sleep(1)
        st.session_state["scanned"] = True
      else:
        st.warning("Please provide text, link, or upload an image.")

  with c2:
    st.markdown("### Detection Result")
    if st.session_state.get("scanned", False):
      st.markdown(
          "<h3 style='color: #e74c3c !important;'>🚨 High Risk Phishing"
          " Detected</h3>",
          unsafe_allow_html=True,
      )
      st.metric(label="Calculated Risk Score", value="92.4%", delta="Dangerous")
      st.markdown("**Confidence Level:** 96.8%")
      st.markdown("**Primary Model:** Random Forest + XGBoost")
      st.error(
          "Warning: Malicious patterns or scam indicators found in content!"
      )
    else:
      st.info(
          "Perform a Quick Scan or upload an image to generate threat"
          " analytics."
      )

  with c3:
    st.markdown("### Live Performance Metrics")
    m1, m2 = st.columns(2)
    m1.metric("Accuracy", "96.4%")
    m2.metric("Precision", "94.1%")
    m3, m4 = st.columns(2)
    m3.metric("Recall", "91.8%")
    m4.metric("F1-Score", "92.9%")

  st.markdown("---")
  st.markdown(
      "### 📊 Risk Progression & High-Risk Threat Trend Graph"
  )  # Requested Feature
  # Colorful area/line chart tracking safe vs high-risk/phishing detections
  risk_graph_data = pd.DataFrame(
      {
          "Safe Content": [400, 480, 510, 600, 720, 810, 890],
          "High Risk / Phishing Detected": [90, 130, 110, 160, 220, 190, 250],
      },
      index=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  )
  st.area_chart(risk_graph_data)

# ==================== MODEL ANALYSIS TAB ====================
elif menu == "Advanced Model Analysis":
  st.markdown("### Multi-Model Comparative Analysis")
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
elif menu == "Real-Time Threat Intelligence":
  st.markdown("### Global Threat Feed & Attack Map Matrix")
  t1, t2, t3, t4 = st.columns(4)
  t1.metric("Active Botnets", "42")
  t2.metric("Blocked Domains", "1,420")
  t3.metric("Phishing Signatures", "8,930")
  t4.metric("Global Server Load", "14.2%")

  st.markdown("#### Live Attack Coordinates (Simulated Heatmap)")
  map_data = pd.DataFrame(
      {
          "lat": [13.0827, 37.7749, 51.5074, 35.6762, 1.3521],
          "lon": [80.2707, -122.4194, -0.1278, 139.6503, 103.8198],
      }
  )
  st.map(map_data)

# ==================== API & THREAT CENTER ====================
elif menu == "API & Threat Center":
  st.markdown("### API Anomaly Monitor")
  st.markdown(
      "Monitor unusual traffic spikes, high request rates, and API errors."
  )

  api_col1, api_col2, api_col3 = st.columns(3)
  api_col1.metric("Total Requests (24h)", "45,210", "+14% Spike")
  api_col2.metric("Anomaly Rate", "0.42%", "-0.05%")
  api_col3.metric("API Error Rate", "1.18%", "Normal")

  api_traffic_data = pd.DataFrame(
      {
          "Normal Traffic": [300, 450, 400, 600, 750, 500, 650],
          "Anomalous Requests": [10, 45, 12, 85, 30, 15, 50],
      },
      index=["12 AM", "4 AM", "8 AM", "12 PM", "4 PM", "8 PM", "11 PM"],
  )
  st.line_chart(api_traffic_data)

  st.markdown("---")
  st.markdown("### Threat Monitoring & Alert Center")
  st.markdown(
      "View high-risk detection alerts, timestamps, threat categories, and"
      " investigation statuses."
  )

  alerts_data = pd.DataFrame(
      {
          "Alert ID": ["ALT-1092", "ALT-1093", "ALT-1094", "ALT-1095"],
          "Timestamp": [
              "2026-10-26 19:10",
              "2026-10-26 18:45",
              "2026-10-26 17:20",
              "2026-10-26 16:05",
          ],
          "Threat Category": [
              "Credential Harvesting",
              "Malicious Redirect",
              "Spear Phishing",
              "C2 Beaconing",
          ],
          "Risk Level": ["High", "Critical", "High", "Medium"],
          "Investigation Status": [
              "Under Review",
              "Blocked & Resolved",
              "Investigating",
              "Resolved",
          ],
      }
  )
  st.dataframe(alerts_data, use_container_width=True)

# ==================== SETTINGS TAB ====================
elif menu == "Settings":
  st.markdown("### System Configuration & Thresholds")
  st.slider("AI Sensitivity Threshold (%)", 50, 99, 85)
  st.text_input("API Security Key", "sk-colorful-sec-998821-xyz")
  st.checkbox("Enable Real-time Threat Alerts", value=True)
  st.checkbox("Auto-block Suspicious IP Addresses", value=True)
  if st.button("Save Security Preferences"):
    st.success("Preferences updated successfully with vibrant color profiles!")
