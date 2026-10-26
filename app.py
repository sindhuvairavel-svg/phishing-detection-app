import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import re
from urllib.parse import urlparse

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="PhishShift | Message Risk Scanner",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- BLACK & GOLD THEME ----------------
st.markdown("""
<style>
.stApp {
    background-color: #080a0f;
    color: #f5f5f5;
}
[data-testid="stSidebar"] {
    background-color: #10131b;
}
h1, h2, h3 {
    color: #f5c542 !important;
}
div[data-testid="stMetric"] {
    background: #141923;
    border: 1px solid #3d3420;
    padding: 15px;
    border-radius: 12px;
}
.stButton > button {
    background-color: #f5c542;
    color: #080a0f;
    border-radius: 8px;
    border: none;
    font-weight: bold;
}
.stButton > button:hover {
    background-color: #ffe082;
    color: #080a0f;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🛡️ PhishShift")
st.caption("MESSAGE RISK SCANNER & SECURITY TRIAGE DASHBOARD")
st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Navigation")

page = st.sidebar.radio(
    "Choose a section",
    [
        "Dashboard Overview",
        "Real-Time Risk Scanner",
        "Multi-Model Selector",
        "Risk Threshold",
        "Threat Monitor",
        "Typo & Attack Sandbox",
        "API Anomaly Monitor",
        "Threat Intelligence",
        "Prompt Injection Shield",
        "Explainable AI",
        "Confidence Calibration",
        "Advanced Security Monitor"
    ]
)

# ---------------- HELPER FUNCTION ----------------
def analyse_message(message):
    """Simple demo heuristic. This is not a trained ML model."""

    text = message.lower()
    score = 0
    reasons = []

    suspicious_words = [
        "verify your account",
        "urgent",
        "click here",
        "password",
        "bank account",
        "suspended",
        "login immediately",
        "claim your prize",
        "otp",
        "free gift",
        "limited time",
        "confirm your identity"
    ]

    for word in suspicious_words:
        if word in text:
            score += 12
            reasons.append(f"Suspicious phrase detected: '{word}'")

    urls = re.findall(r"https?://\S+|www\.\S+", message)

    if urls:
        score += 15
        reasons.append("Message contains a URL")

    if re.search(r"\b(password|otp|pin|bank details)\b", text):
        score += 15
        reasons.append("Possible request for sensitive information")

    if message.count("!") >= 3:
        score += 8
        reasons.append("Excessive exclamation marks")

    if len(message) > 0 and message.isupper():
        score += 10
        reasons.append("Entire message is uppercase")

    score = min(score, 100)

    if score >= 60:
        label = "HIGH RISK"
    elif score >= 30:
        label = "MEDIUM RISK"
    else:
        label = "LOW RISK"

    if not reasons:
        reasons.append("No obvious suspicious patterns detected")

    return score, label, reasons


# ---------------- DASHBOARD OVERVIEW ----------------
if page == "Dashboard Overview":
    st.header("Dashboard Overview")
    st.write(
        "Monitor message risks, suspicious patterns, and security signals "
        "from one dashboard."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Scanner Status", "READY")
    col2.metric("Detection Mode", "Rule-Based Demo")
    col3.metric("Risk Categories", "3")
    col4.metric("Security Modules", "12")

    st.markdown("### Security Modules")

    c1, c2 = st.columns(2)

    with c1:
        st.info("🛡️ Real-Time Risk Scanner")
        st.info("🤖 Multi-Model Selector")
        st.info("🎚️ Risk Threshold Control")
        st.info("📈 Threat Monitor")
        st.info("🔤 Typo & Attack Sandbox")
        st.info("🔥 API Anomaly Monitor")

    with c2:
        st.info("🌐 URL Pattern Checker")
        st.info("🚨 Prompt Injection Shield")
        st.info("🔍 Explainable AI")
        st.info("📊 Confidence Calibration")
        st.info("🔐 Advanced Security Monitor")
        st.info("⚙️ Detection Settings")

    st.warning(
        "Demo version: results are generated using simple rules, "
        "not a trained machine-learning model or live threat-intelligence service."
    )


# ---------------- REAL-TIME RISK SCANNER ----------------
elif page == "Real-Time Risk Scanner":
    st.header("🔎 Real-Time Message Risk Scanner")

    message = st.text_area(
        "Paste a message to analyse",
        placeholder="Example: Your account is suspended. Verify your account immediately.",
        height=160
    )

    if st.button("SCAN MESSAGE"):
        if not message.strip():
            st.warning("Please enter a message first.")
        else:
            score, label, reasons = analyse_message(message)

            col1, col2 = st.columns(2)

            col1.metric("Risk Score", f"{score}/100")
            col2.metric("Risk Classification", label)

            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=score,
                    title={"text": "Message Risk Level"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "#f5c542"},
                        "steps": [
                            {"range": [0, 30], "color": "#164e36"},
                            {"range": [30, 60], "color": "#70551b"},
                            {"range": [60, 100], "color": "#702727"}
                        ]
                    }
                )
            )

            fig.update_layout(
                paper_bgcolor="#080a0f",
                font_color="white",
                height=300
            )

            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Why was this result produced?")

            for reason in reasons:
                st.write("•", reason)

            if score >= 60:
                st.error("High-risk patterns detected. Verify the message independently.")
            elif score >= 30:
                st.warning("Some suspicious patterns were found. Check carefully.")
            else:
                st.success("Few suspicious patterns were found.")

            st.caption(
                "A low score does not guarantee that a message is safe."
            )


# ---------------- MULTI-MODEL SELECTOR ----------------
elif page == "Multi-Model Selector":
    st.header("🤖 Detection Model Selector")

    model = st.selectbox(
        "Choose a demonstration profile",
        [
            "Balanced Detection",
            "High Sensitivity",
            "Low False-Alarm Mode",
            "Fast Screening"
        ]
    )

    details = {
        "Balanced Detection":
            "Balances suspicious-message detection and false alarms.",
        "High Sensitivity":
            "Designed to flag more suspicious messages, but may flag more safe messages too.",
        "Low False-Alarm Mode":
            "Uses a more cautious approach before marking a message suspicious.",
        "Fast Screening":
            "A simple, lightweight screening profile."
    }

    st.subheader(model)
    st.write(details[model])

    st.warning(
        "These are demonstration profiles. They do not load separate trained AI models."
    )


# ---------------- RISK THRESHOLD ----------------
elif page == "Risk Threshold":
    st.header("🎚️ Risk Threshold Control")

    threshold = st.slider(
        "Choose the risk score at which a message is flagged",
        min_value=10,
        max_value=90,
        value=60,
        step=5
    )

    st.metric("Selected Threshold", f"{threshold}/100")

    sample_score = st.slider(
        "Try a sample risk score",
        min_value=0,
        max_value=100,
        value=45
    )

    if sample_score >= threshold:
        st.error("This sample would be flagged for review.")
    else:
        st.success("This sample would not be flagged by this threshold.")

    st.caption(
        "A lower threshold flags more messages; a higher threshold may miss some threats."
    )


# ---------------- THREAT MONITOR ----------------
elif page == "Threat Monitor":
    st.header("📈 False-Positive & Attack Trend Monitor")

    st.write("Illustrative demonstration data — not live security telemetry.")

    dates = pd.date_range(end=pd.Timestamp.today(), periods=7)

    data = pd.DataFrame({
        "Day": dates.strftime("%a"),
        "Flagged Messages": np.random.randint(10, 60, 7),
        "False Alarms": np.random.randint(1, 15, 7),
        "Attack Attempts": np.random.randint(5, 45, 7)
    })

    st.line_chart(
        data.set_index("Day")[[
            "Flagged Messages",
            "False Alarms",
            "Attack Attempts"
        ]]
    )

    st.dataframe(data, use_container_width=True, hide_index=True)


# ---------------- TYPO & ATTACK SANDBOX ----------------
elif page == "Typo & Attack Sandbox":
    st.header("🔤 Typo & Perturbation Sandbox")

    original = st.text_input(
        "Enter a sample message",
        value="Verify your account immediately"
    )

    variation = st.selectbox(
        "Choose a test variation",
        [
            "Original Text",
            "Uppercase Text",
            "Extra Exclamation Marks",
            "Extra Spaces"
        ]
    )

    if variation == "Uppercase Text":
        modified = original.upper()
    elif variation == "Extra Exclamation Marks":
        modified = original + "!!!"
    elif variation == "Extra Spaces":
        modified = "  ".join(original.split())
    else:
        modified = original

    st.subheader("Modified Message")
    st.code(modified)

    score, label, reasons = analyse_message(modified)

    col1, col2 = st.columns(2)
    col1.metric("Risk Score", f"{score}/100")
    col2.metric("Risk Label", label)

    st.write("Detected patterns:")
    for reason in reasons:
        st.write("•", reason)


# ---------------- API ANOMALY MONITOR ----------------
elif page == "API Anomaly Monitor":
    st.header("🔥 API Anomaly & Threat Velocity Monitor")

    st.write("Synthetic sample data for interface demonstration.")

    rows = ["API-1", "API-2", "API-3", "API-4", "API-5"]
    columns = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00"]

    heatmap_data = np.random.randint(0, 100, (len(rows), len(columns)))

    fig = go.Figure(
        data=go.Heatmap(
            z=heatmap_data,
            x=columns,
            y=rows,
            colorscale=[
                [0, "#142d25"],
                [0.5, "#9c7622"],
                [1, "#b83232"]
            ],
            colorbar={"title": "Activity"}
        )
    )

    fig.update_layout(
        paper_bgcolor="#080a0f",
        plot_bgcolor="#080a0f",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "To monitor real API activity, connect this page to actual server logs or monitoring data."
    )


# ---------------- THREAT INTELLIGENCE ----------------
elif page == "Threat Intelligence":
    st.header("🌐 URL Pattern Checker")

    url = st.text_input(
        "Enter a URL to inspect",
        placeholder="https://example.com"
    )

    if st.button("CHECK URL"):
        if not url.strip():
            st.warning("Please enter a URL.")
        else:
            check_url = url.strip()

            if not check_url.startswith(("http://", "https://")):
                check_url = "https://" + check_url

            parsed = urlparse(check_url)
            domain = parsed.netloc.lower()
            findings = []

            if not domain:
                findings.append("URL format appears invalid.")

            if parsed.scheme == "http":
                findings.append("The URL uses HTTP rather than HTTPS.")

            if "@" in check_url:
                findings.append("The URL contains an @ symbol.")

            if len(domain) > 45:
                findings.append("The domain name is unusually long.")

            if any(char.isdigit() for char in domain):
                findings.append("The domain contains numeric characters.")

            if domain.count("-") >= 3:
                findings.append("The domain contains several hyphens.")

            if not findings:
                st.success("No obvious URL warning patterns detected.")
            else:
                for finding in findings:
                    st.warning(finding)

            st.caption(
                "This is a basic URL-pattern check. It does not verify the URL against live threat-intelligence databases. Do not open suspicious links."
            )


# ---------------- PROMPT INJECTION SHIELD ----------------
elif page == "Prompt Injection Shield":
    st.header("🚨 Prompt Injection & Jailbreak Shield")

    prompt = st.text_area(
        "Enter text to inspect",
        placeholder="Paste text you want to check for suspicious instruction patterns.",
        height=150
    )

    if st.button("INSPECT TEXT"):
        lowered = prompt.lower()

        patterns = [
            "ignore all previous instructions",
            "reveal your system prompt",
            "bypass security",
            "ignore the rules",
            "reveal confidential information",
            "act as an unrestricted ai",
            "disregard previous instructions"
        ]

        found = [p for p in patterns if p in lowered]

        if found:
            st.error("Potential prompt-injection patterns detected.")
            for item in found:
                st.write("•", item)
        else:
            st.success("No listed prompt-injection phrases were detected.")

        st.caption(
            "This phrase checker is only a basic demonstration and cannot detect every attack."
        )


# ---------------- EXPLAINABLE AI ----------------
elif page == "Explainable AI":
    st.header("🔍 Explainable AI (XAI)")

    st.write(
        "This section explains which visible text patterns contributed to a demo risk score."
    )

    message = st.text_area(
        "Enter a message",
        placeholder="Your account is suspended. Verify your account now."
    )

    if st.button("EXPLAIN RESULT"):
        if message.strip():
            score, label, reasons = analyse_message(message)

            st.metric("Risk Score", f"{score}/100")
            st.metric("Classification", label)

            st.subheader("Contributing Signals")

            for reason in reasons:
                st.write("🔸", reason)
        else:
            st.warning("Enter a message to explain.")


# ---------------- CONFIDENCE CALIBRATION ----------------
elif page == "Confidence Calibration":
    st.header("📊 Confidence Calibration")

    st.write(
        "Explore how a hypothetical confidence value maps to a display category."
    )

    confidence = st.slider(
        "Sample confidence",
        min_value=0,
        max_value=100,
        value=75
    )

    st.metric("Sample Confidence", f"{confidence}%")

    if confidence >= 80:
        st.success("High confidence in this demonstration value.")
    elif confidence >= 50:
        st.warning("Medium confidence in this demonstration value.")
    else:
        st.error("Low confidence in this demonstration value.")

    st.caption(
        "This is an illustrative slider, not a calibrated probability from a trained model."
    )


# ---------------- ADVANCED SECURITY MONITOR ----------------
elif page == "Advanced Security Monitor":
    st.header("🔐 Advanced Security Monitor")

    st.write("Enter sample counts to calculate simple monitoring indicators.")

    col1, col2 = st.columns(2)

    with col1:
        total = st.number_input(
            "Total messages checked",
            min_value=0,
            max_value=1000000,
            value=100
        )

    with col2:
        flagged = st.number_input(
            "Messages flagged",
            min_value=0,
            max_value=1000000,
            value=15
        )

    if st.button("CALCULATE INDICATORS"):
        if total == 0:
            st.warning("Total messages must be greater than zero.")
        elif flagged > total:
            st.warning("Flagged messages cannot exceed total messages.")
        else:
            rate = (flagged / total) * 100

            col1, col2 = st.columns(2)
            col1.metric("Flagged Messages", int(flagged))
            col2.metric("Flagged Rate", f"{rate:.2f}%")

            st.progress(min(rate / 100, 1.0))

            st.caption(
                "This is a simple count-based indicator, not a verified threat detection rate."
            )


# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "PhishShift | Educational Prototype | Rule-Based Demo | "
    "Not a substitute for verified security tools"
)
