import time
import random
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Advanced Next-Gen Phishing Detection Hub",
    page_icon="🛡️",
    layout="wide",
)

# Custom Styling (Dark Gold, Colorful Accents, No Harsh Boxes)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #050505;
        color: #f0f2f6;
    }
    section[data-testid="stSidebar"] {
        background-color: #0b0b0b;
        border-right: 2px solid #d4af37;
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #d4af37 !important;
        font-weight: bold;
    }
    /* Remove harsh box borders */
    div[data-testid="stVerticalBlock"] > div {
        background-color: transparent;
        border: none;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #d4af37 !important;
    }
    /* Vibrant Gold & Green Gradient Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #d4af37 0%, #2ecc71 100%);
        color: #050505 !important;
        font-weight: bold;
        border-radius: 6px;
        border: none;
        padding: 10px 20px;
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.4);
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #f3e5ab 0%, #27ae60 100%);
    }
    /* Clean Input Fields */
    input, textarea, div[data-baseweb="select"] {
        background-color: #141414 !important;
        color: #d4af37 !important;
        border: 1px solid #d4af37 !important;
        border-radius: 6px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar Navigation
st.sidebar.markdown(
    "<h2 style='text-align: center; color: #d4af37;'>🛡️ NEXT-GEN AI</h2>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<p style='text-align: center; color: #2ecc71;'>Advanced Phishing"
    " Defense</p>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation Menu",
    [
        "🏠 Next-Gen Scanner & XAI",
        "📊 Threat & Risk Analytics",
        "🌐 Global Threat Intel",
        "🛡️ API & Alert Center",
        "⚙️ System Settings",
    ],
)

# Top Header
col_title, col_status = st.columns([3, 1])
with col_title:
  st.markdown("## 🛡️ AI-Powered Phishing Detection & Threat Intelligence Hub")
with col_status:
  st.markdown(
      "🟢 **System Online**  \n⚡ Zero-Day Protection Active",
      unsafe_allow_html=True,
  )

st.markdown("---")

# ==================== TAB 1: SCANNER & XAI ====================
if menu == "🏠 Next-Gen Scanner & XAI":
  c1, c2, c3 = st.columns([1.2, 1.2, 1.1])

  with c1:
    st.markdown("### ⚡ Multi-Modal Threat Scanner")
    scan_mode = st.radio(
        "Detection Input",
        [
            "Text / URL / Email",
            "Upload Screenshot (OCR Logo Check)",
            "QR Phishing (Quishing)",
        ],
    )

    if scan_mode == "Text / URL / Email":
      user_text = st.text_area(
          "Paste suspicious content or link:",
          placeholder="e.g., https://secure-bank-login-verify.com",
          height=110,
      )
    elif scan_mode == "Upload Screenshot (OCR Logo Check)":
      uploaded_file = st.file_uploader(
          "Upload Image for Brand Impersonation Scan",
          type=["png", "jpg", "jpeg"],
      )
      user_text = "Image uploaded for OCR & Logo analysis" if uploaded_file else ""
    else:
      qr_file = st.file_uploader("Upload QR Code Image", type=["png", "jpg"])
      user_text = "QR Code uploaded for Quishing check" if qr_file else ""

    if st.button("Run Advanced Deep Scan"):
      if user_text:
        with st.spinner(
            "Running Zero-Day Analysis, OCR, & Ensemble AI Models..."
        ):
          time.sleep(1)
        st.session_state["scanned"] = True
      else:
        st.warning("Please provide input data or upload a file.")

  with c2:
    st.markdown("### 🎯 Threat & Risk Verdict")
    if st.session_state.get("scanned", False):
      st.markdown(
          "<h3 style='color: #ff3333 !important;'>🚨 HIGH RISK: Phishing &"
          " Scam Detected</h3>",
          unsafe_allow_html=True,
      )
      st.metric(
          label="Calculated Risk Score", value="94.8%", delta="+18.4% Critical"
      )
      st.markdown("**Domain Age:** < 24 Hours (Suspicious)")
      st.markdown("**Explainable AI (SHAP):** Triggered by 'Verify Login' keyword")
      st.error(
          "Warning: Malicious brand spoofing and C2 redirect patterns found!"
      )
    else:
      st.info(
          "Run a Deep Scan to view risk scores and Explainable AI breakdown."
      )

  with c3:
    st.markdown("### 📈 Live Model Metrics")
    m1, m2 = st.columns(2)
    m1.metric("Ensemble Accuracy", "98.2%")
    m2.metric("False Positive Rate", "0.12%")
    m3, m4 = st.columns(2)
    m3.metric("Zero-Day Catch", "95.6%")
    m4.metric("OCR Precision", "96.4%")

  st.markdown("---")
  st.markdown("### 📊 Real-Time Risk Progression & Threat Trend Graph")
  # Colorful area chart tracking safe vs high risk threats over the week
  risk_trend_data = pd.DataFrame(
      {
          "Safe Verified Content": [500, 620, 590, 710, 840, 910, 980],
          "High Risk / Phishing Caught": [110, 140, 95, 180, 240, 210, 290],
      },
      index=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  )
  st.area_chart(risk_trend_data)

# ==================== TAB 2: MODEL & RISK ANALYTICS ====================
elif menu == "📊 Threat & Risk Analytics":
  st.markdown("### 📊 Advanced Model Comparison & Feature Importance")
  model_perf = pd.DataFrame(
      {
          "AI Classifier": [
              "XGBoost + Transformer",
              "Random Forest",
              "Neural Network (CNN)",
              "SVM",
              "Naive Bayes",
          ],
          "Accuracy (%)": [98.2, 97.4, 96.1, 92.5, 88.0],
      }
  )
  st.bar_chart(model_perf.set_index("AI Classifier")["Accuracy (%)"])
  st.dataframe(model_perf, use_container_width=True)

# ==================== TAB 3: THREAT INTELLIGENCE ====================
elif menu == "🌐 Global Threat Intelligence":
  st.markdown("### 🌐 Global Attack Map & Dark Web Credential Scanner")
  t1, t2, t3, t4 = st.columns(4)
  t1.metric("Active C2 Servers", "58")
  t2.metric("Dark Web Leaks", "1,240")
  t3.metric("Quishing Vectors", "310")
  t4.metric("Global Firewall Load", "18.4%")

  st.markdown("#### 🌍 Live Global Attack Coordinates")
  map_data = pd.DataFrame(
      {
          "lat": [13.0827, 37.7749, 51.5074, 35.6762, 1.3521, -33.8688],
          "lon": [80.2707, -122.4194, -0.1278, 139.6503, 103.8198, 151.2093],
      }
  )
  st.map(map_data)

# ==================== TAB 4: API & ALERT CENTER ====================
elif menu == "🛡️ API & Alert Center":
  st.markdown("### 🔌 API Anomaly & Traffic Telemetry Monitor")
  ac1, ac2, ac3 = st.columns(3)
  ac1.metric("API Requests (24h)", "62,400", "+22% Spike")
  ac2.metric("Anomaly Rate", "0.28%", "-0.08%")
  ac3.metric("Blocked Payload Errors", "0.92%", "Secured")

  api_df = pd.DataFrame(
      {
          "Normal Traffic": [400, 550, 500, 700, 900, 650, 800],
          "Anomalous Traffic Spikes": [15, 60, 20, 110, 40, 25, 75],
      },
      index=["12 AM", "4 AM", "8 AM", "12 PM", "4 PM", "8 PM", "11 PM"],
  )
  st.line_chart(api_df)

  st.markdown("---")
  st.markdown("### 🚨 Threat Monitoring & Active Incident Alert Center")
  alerts_table = pd.DataFrame(
      {
          "Incident ID": ["INC-901", "INC-902", "INC-903", "INC-904"],
          "Timestamp": [
              "2026-10-26 21:14",
              "2026-10-26 20:30",
              "2026-10-26 19:12",
              "2026-10-26 17:45",
          ],
          "Threat Category": [
              "Zero-Day Credential Phishing",
              "Visual Brand Spoofing (OCR)",
              "Quishing (QR Code Scam)",
              "C2 Beaconing Anomaly",
          ],
          "Risk Severity": ["Critical", "High", "High", "Medium"],
          "Investigation Status": [
              "Blocked & Investigating",
              "Resolved",
              "Under Review",
              "Mitigated",
          ],
      }
  )
  st.dataframe(alerts_table, use_container_width=True)

# ==================== TAB 5: SETTINGS ====================
elif menu == "⚙️ System Settings":
  st.markdown("### ⚙️ AI Engine & Security Configuration")
  st.slider("Zero-Day AI Sensitivity Threshold (%)", 50, 99, 90)
  st.text_input("Enterprise Security API Key", "sk-nextgen-gold-sec-778899")
  st.checkbox("Enable Automated IP Auto-Blocking", value=True)
  st.checkbox("Enable Explainable AI (SHAP) Breakdowns", value=True)
  if st.button("Save System Configuration"):
    st.success(
        "Next-generation security configurations updated successfully!"
    )
