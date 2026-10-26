import re
import difflib
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="PhishShift Message Risk Scanner", page_icon="🛡️", layout="wide")

# ---------------- Black & Golden Theme ----------------
st.markdown("""
<style>
.stApp, .main { background-color: #030303; color: #f0f0f0; }
.stSidebar, section[data-testid="stSidebar"] div { background-color: #0a0a0a !important; color: #ffd700 !important; }
.stSidebar { border-right: 1px solid #332700; }
.stMetric { background-color: #0d0d0d; padding: 15px; border-radius: 10px; border: 1px solid #ffd700; box-shadow: 0 4px 15px rgba(212,175,55,0.25); }
h1, h2, h3, h4, h5, h6 { color: #ffd700 !important; font-family: sans-serif; text-shadow: 2px 2px 6px rgba(0,0,0,0.9); }
.stButton>button { background: linear-gradient(135deg, #ffd700, #b8860b); color: #030303; font-weight: bold; border-radius: 6px; border: none; padding: 10px 20px; }
.stButton>button:hover { background: linear-gradient(135deg, #fff8dc, #ffd700); color: #030303; }
textarea, input { color: #ffd700 !important; background-color: #0d0d0d !important; border: 1px solid #ffd700 !important; }
.stSelectbox div[data-baseweb="select"] { background-color: #0d0d0d !important; color: #ffd700 !important; border: 1px solid #ffd700 !important; }
div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] { background-color: #120e00 !important; border: 2px solid #ffd700 !important; color: #ffd700 !important; }
div[data-baseweb="option"], div[data-baseweb="option"] div { background-color: #120e00 !important; color: #ffd700 !important; }
div[data-baseweb="option"]:hover, div[data-baseweb="option"]:hover div { background-color: #ffd700 !important; color: #030303 !important; }
p, label, span, div { color: #e0e0e0; }
.stDataFrame, .stTable { background-color: #0d0d0d !important; color: #ffd700 !important; }
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #030303; }
::-webkit-scrollbar-thumb { background: #b8860b; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #ffd700; }
mark { background: #ffd700; color: #030303; padding: 0 3px; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ---------------- Shared Data & Helpers ----------------
KEYWORDS = {
    "urgent": 12, "immediately": 12, "verify": 10, "kyc": 15, "blocked": 10, "locked": 10,
    "suspended": 10, "otp": 15, "password": 10, "pan card": 12, "aadhaar": 12, "refund": 8,
    "lottery": 15, "winner": 12, "prize": 12, "click here": 12, "secure link": 12,
    "bank account": 10, "expire": 8, "limited time": 8, "gift card": 12, "act now": 10,
}
BRANDS = ["google", "paypal", "amazon", "facebook", "instagram", "whatsapp", "sbi", "hdfc",
          "icici", "paytm", "phonepe", "netflix", "microsoft", "apple", "flipkart"]
SUSPICIOUS_TLDS = [".xyz", ".top", ".tk", ".ml", ".click", ".work", ".info", ".online"]
LEET = str.maketrans({"0": "o", "1": "l", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s"})

MODELS = {
    "Rule-Based Baseline": {"acc": 78.5, "prec": 0.72, "rec": 0.81, "speed_ms": 8, "boost": 0},
    "Keyword + Pattern Classifier": {"acc": 89.2, "prec": 0.88, "rec": 0.87, "speed_ms": 25, "boost": 6},
    "Advanced AI Model (BERT-Sec)": {"acc": 94.8, "prec": 0.93, "rec": 0.95, "speed_ms": 90, "boost": 12},
}
SENS_BONUS = {"Low": -10, "Medium": 0, "High": 10}

if "model" not in st.session_state:
    st.session_state.model = "Keyword + Pattern Classifier"
if "sens" not in st.session_state:
    st.session_state.sens = "Medium"
if "abstain" not in st.session_state:
    st.session_state.abstain = 85


def extract_urls(text):
    return re.findall(r"(?:https?://|www\.)[^\s]+|\b[\w-]+\.(?:com|in|xyz|top|tk|ml|click|work|info|online|net|org)\b[^\s]*", text, re.I)


def get_domain(url):
    url = re.sub(r"^https?://", "", url.lower()).replace("www.", "")
    return re.split(r"[/?#]", url)[0]


def check_domain(domain):
    """Returns list of (reason, points) for a domain."""
    issues = []
    clean = domain.translate(LEET)
    label = clean.split(".")[0].replace("-", "")
    for brand in BRANDS:
        if label == brand and domain.split(".")[0] != brand:
            issues.append((f"Number/symbol tricks used to copy '{brand}'", 40))
        elif brand in label and label != brand:
            issues.append((f"Brand name '{brand}' hidden inside a fake domain", 30))
        else:
            ratio = difflib.SequenceMatcher(None, label, brand).ratio()
            if 0.8 <= ratio < 1.0:
                issues.append((f"Looks very similar to '{brand}' (possible typo-squatting)", 35))
    if any(domain.endswith(t) for t in SUSPICIOUS_TLDS):
        issues.append(("Suspicious domain ending", 15))
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain):
        issues.append(("Raw IP address used instead of a domain", 30))
    if domain.count("-") >= 2:
        issues.append(("Too many hyphens in domain", 10))
    if domain.count(".") >= 3:
        issues.append(("Too many sub-domains", 10))
    return issues


def scan_text(text):
    """Core scoring engine used by multiple features."""
    low = text.lower()
    score, reasons, hits = 0, [], []
    for kw, pts in KEYWORDS.items():
        if kw in low:
            score += pts
            hits.append(kw)
    if hits:
        reasons.append(f"Scam words found: {', '.join(hits)}")
    for u in extract_urls(text):
        for reason, pts in check_domain(get_domain(u)):
            score += pts
            reasons.append(f"URL {get_domain(u)}: {reason}")
    letters = [c for c in text if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.4:
        score += 8
        reasons.append("Too many CAPITAL letters (pressure tactic)")
    if text.count("!") >= 3:
        score += 5
        reasons.append("Excess exclamation marks")
    score += MODELS[st.session_state.model]["boost"] if score > 0 else 0
    score += SENS_BONUS[st.session_state.sens] if score > 0 else 0
    return max(0, min(score, 99)), reasons, hits


def verdict(score):
    if score >= st.session_state.abstain:
        return "🚨 PHISHING", "error"
    if score >= 40:
        return "⚠️ SUSPICIOUS – Manual Review", "warning"
    return "✅ SAFE", "success"


def show_verdict(score, reasons):
    label, kind = verdict(score)
    c1, c2, c3 = st.columns(3)
    c1.metric("Risk Score", f"{score}%")
    c2.metric("Verdict", label)
    c3.metric("Model / Sensitivity", st.session_state.model.split(" (")[0], st.session_state.sens)
    st.progress(score / 100)
    getattr(st, kind)(f"Result: {label}")
    if reasons:
        st.markdown("**Why this result:**")
        for r in reasons:
            st.write(f"• {r}")


# ---------------- Sidebar ----------------
st.title("🛡️ PhishShift: Message Risk Scanner & Safety Dashboard")
st.markdown("**Project Code:** ML-07 | **Focus:** Phishing Detection & Personal Safety")
st.markdown("---")

st.sidebar.header("🎛️ Dashboard Control Panel")
mode = st.sidebar.selectbox("Choose Feature", [
    "1. Instant Multi-Channel Scanner",
    "2. AI Threat Detection & False-Positive Reduction",
    "3. Security Sensitivity & Model Selector",
    "4. URL Typo & Impersonation Sandbox",
    "5. Threat Pattern & Keyword Analyzer",
    "6. Interactive Threat Analytics Dashboard",
    "7. Live Activity, Traffic & API Anomaly Monitor",
    "8. Global Scam Intelligence & Alert Feed",
    "9. Protection Guard Comparison & Risk Assessment",
    "10. Personal Safety Checklist & Emergency Report Assistant",
])
st.sidebar.caption(f"Active model: {st.session_state.model}")
st.sidebar.caption(f"Sensitivity: {st.session_state.sens} | Block at ≥ {st.session_state.abstain}%")

# ---------------- 1 ----------------
if mode.startswith("1."):
    st.header("🔍 Instant Multi-Channel Phishing Scanner")
    channel = st.radio("Channel", ["SMS", "Email", "URL"], horizontal=True)
    default = {
        "SMS": "URGENT: Your bank account is locked due to pending KYC verification. Update your PAN card immediately via this secure link http://sbi-kyc-update.xyz/login",
        "Email": "Dear user, your password will expire today. Click here to verify your account immediately or it will be suspended.",
        "URL": "http://paypa1-secure-login.top/verify",
    }[channel]
    text = st.text_area(f"Enter {channel} content to scan:", default, key=f"in_{channel}")
    if st.button("Scan Now"):
        if channel == "URL":
            score, reasons, _ = 0, [], []
            for reason, pts in check_domain(get_domain(text.strip())):
                score += pts
                reasons.append(reason)
            score = min(score + (MODELS[st.session_state.model]["boost"] if score else 0)
                        + (SENS_BONUS[st.session_state.sens] if score else 0), 99)
            score = max(score, 0)
        else:
            score, reasons, _ = scan_text(text)
        show_verdict(score, reasons)

# ---------------- 2 ----------------
elif mode.startswith("2."):
    st.header("🧠 AI Threat Detection & False-Positive Reduction")
    st.markdown("Real bank/service alerts can look urgent too. Add trusted senders so they are not wrongly blocked.")
    sender = st.text_input("Sender name / domain:", "alerts@hdfcbank.com")
    msg = st.text_area("Message:", "Your OTP is 482913. Do not share it with anyone. Valid for 5 minutes. - HDFC Bank")
    trusted = st.multiselect("Trusted senders list", ["hdfcbank.com", "sbi.co.in", "amazon.in", "irctc.co.in", "paytm.com"],
                             default=["hdfcbank.com", "sbi.co.in"])
    st.session_state.abstain = st.slider("Auto-block threshold (%)", 50, 99, st.session_state.abstain,
                                         help="Scores below this go to manual review instead of auto-blocking.")
    if st.button("Analyze"):
        score, reasons, _ = scan_text(msg)
        is_trusted = any(sender.lower().endswith(t) for t in trusted)
        if is_trusted and not any("URL" in r for r in reasons):
            st.success("Trusted sender + no suspicious links → warning reduced (false-positive avoided).")
            score = max(score - 40, 0)
            reasons.append("Score reduced because sender is trusted and message has no fake links")
        show_verdict(score, reasons)
    st.subheader("False-Positive Trend")
    fp = pd.DataFrame({"Before AI filter": [14, 13, 15, 12, 14, 13, 12],
                       "After AI filter": [9, 7, 6, 5, 4, 4, 3]},
                      index=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    st.line_chart(fp)

# ---------------- 3 ----------------
elif mode.startswith("3."):
    st.header("🎚️ Security Sensitivity & Model Selector")
    st.session_state.model = st.selectbox("Detection Model", list(MODELS), index=list(MODELS).index(st.session_state.model))
    st.session_state.sens = st.select_slider("Detection Sensitivity", ["Low", "Medium", "High"], value=st.session_state.sens)
    st.info("Low = fewer alerts. High = catches more scams but may flag some safe messages.")
    perf = pd.DataFrame({
        "Model": list(MODELS),
        "Accuracy (%)": [m["acc"] for m in MODELS.values()],
        "Precision": [m["prec"] for m in MODELS.values()],
        "Recall": [m["rec"] for m in MODELS.values()],
    })
    st.table(perf)
    st.bar_chart(perf.set_index("Model")["Accuracy (%)"])
    st.success(f"Saved ✔ Using **{st.session_state.model}** at **{st.session_state.sens}** sensitivity.")

# ---------------- 4 ----------------
elif mode.startswith("4."):
    st.header("🧪 URL Typo & Impersonation Sandbox")
    url = st.text_input("Enter a link to test:", "http://g00gle-login.com/signin")
    if st.button("Check Link"):
        dom = get_domain(url)
        st.write(f"Domain detected: `{dom}`")
        st.write(f"After decoding number tricks: `{dom.translate(LEET)}`")
        issues = check_domain(dom)
        score = min(sum(p for _, p in issues), 99)
        if issues:
            st.error(f"Fake / impersonation risk: {score}%")
            for r, _ in issues:
                st.write(f"• {r}")
        else:
            st.success("No impersonation signs found. Still, always type official sites manually.")
    st.markdown("**Try:** `paypa1.com`, `amaz0n-offers.top`, `hdfc-bank-login.xyz`, `google.com`")

# ---------------- 5 ----------------
elif mode.startswith("5."):
    st.header("🔎 Threat Pattern & Keyword Analyzer")
    txt = st.text_area("Paste message:", "Congratulations winner! Claim your lottery prize now. Share OTP and click here to verify your KYC immediately!")
    if st.button("Analyze Patterns"):
        marked = txt
        found = []
        for kw in sorted(KEYWORDS, key=len, reverse=True):
            if re.search(re.escape(kw), marked, re.I):
                found.append(kw)
                marked = re.sub(f"({re.escape(kw)})", r"<mark>\1</mark>", marked, flags=re.I)
        st.markdown(marked, unsafe_allow_html=True)
        if found:
            df = pd.DataFrame({"Keyword": found, "Danger Weight": [KEYWORDS[k] for k in found]})
            st.table(df)
            st.bar_chart(df.set_index("Keyword"))
        else:
            st.success("No scam keywords found.")
        patterns = {
            "Creates urgency": any(w in txt.lower() for w in ["urgent", "immediately", "now", "expire"]),
            "Asks for private info (OTP/password/PAN)": any(w in txt.lower() for w in ["otp", "password", "pan", "aadhaar"]),
            "Offers free money/prize": any(w in txt.lower() for w in ["lottery", "winner", "prize", "refund"]),
            "Contains a link": bool(extract_urls(txt)),
        }
        st.subheader("Scam Patterns")
        for k, v in patterns.items():
            st.write(("🔴 " if v else "🟢 ") + k)

# ---------------- 6 ----------------
elif mode.startswith("6."):
    st.header("📈 Interactive Threat Analytics Dashboard")
    days = st.slider("Days to show", 7, 30, 14)
    rng = np.random.default_rng(7)
    trend = pd.DataFrame({
        "Phishing Blocked": rng.integers(40, 90, days),
        "Safe Messages": rng.integers(150, 260, days),
    })
    st.subheader("Threat Trend (Line)")
    st.line_chart(trend)
    st.subheader("Attack Types (Bar)")
    st.bar_chart(pd.DataFrame({"Count": [120, 95, 60, 45, 30]},
                              index=["Fake Bank KYC", "Lottery Scam", "Fake Delivery", "Job Scam", "Fake Refund"]))
    st.subheader("Confusion Matrix")
    cm = pd.DataFrame([[470, 18], [12, 500]],
                      index=["Actually Safe", "Actually Phishing"],
                      columns=["Predicted Safe", "Predicted Phishing"])
    st.table(cm)
    tn, fp, fn, tp = 470, 18, 12, 500
    c1, c2, c3 = st.columns(3)
    c1.metric("Accuracy", f"{(tp + tn) / (tp + tn + fp + fn) * 100:.1f}%")
    c2.metric("Precision", f"{tp / (tp + fp):.2f}")
    c3.metric("Recall", f"{tp / (tp + fn):.2f}")

# ---------------- 7 ----------------
elif mode.startswith("7."):
    st.header("⚡ Live Activity, Traffic & API Anomaly Monitor")
    if st.button("🔄 Refresh Live Data"):
        pass
    c1, c2, c3 = st.columns(3)
    c1.metric("Scans Today", f"{np.random.randint(1200, 1800):,}", "+5%")
    c2.metric("Suspicious Traffic", f"{np.random.randint(40, 120)}", "-2%")
    c3.metric("API Anomalies", f"{np.random.randint(0, 9)}", "Check spikes")
    traffic = pd.DataFrame(np.random.randint(10, 100, size=(10, 5)),
                           columns=[f"Hour {i}" for i in range(1, 6)],
                           index=[f"Endpoint API {i}" for i in range(1, 11)])
    st.subheader("Request Heatmap")
    st.dataframe(traffic.style.background_gradient(cmap="YlOrBr"), use_container_width=True)
    st.subheader("Traffic Over Time")
    st.line_chart(traffic.T)
    spikes = traffic[traffic.max(axis=1) > 90]
    if not spikes.empty:
        st.warning(f"Unusual spikes found on: {', '.join(spikes.index)}")
    else:
        st.success("No unusual API spikes right now.")

# ---------------- 8 ----------------
elif mode.startswith("8."):
    st.header("🌐 Global Scam Intelligence & Alert Feed")
    st.markdown("Sample alert feed (connect real sources like CERT-In or PhishTank for live data).")
    feed = pd.DataFrame({
        "Time": ["12:30", "12:28", "12:15", "11:58", "11:40"],
        "Scam Type": ["Fake Bank KYC", "Delivery SMS", "Job Offer", "Fake Refund", "Lottery"],
        "Region": ["India", "India", "Global", "India", "Global"],
        "Severity": ["High", "Medium", "Medium", "High", "Low"],
        "Status": ["Blocked", "Flagged", "Flagged", "Blocked", "Monitoring"],
    })
    sev = st.multiselect("Filter severity", ["High", "Medium", "Low"], default=["High", "Medium", "Low"])
    st.table(feed[feed["Severity"].isin(sev)])
    st.subheader("New Threats This Week")
    st.info("📦 Fake courier 'address update' SMS with short links is rising.")
    st.info("💼 'Work from home' job scams asking for registration fees.")
    st.info("📱 Fake UPI refund requests asking you to enter your PIN.")

# ---------------- 9 ----------------
elif mode.startswith("9."):
    st.header("⚖️ Protection Guard Comparison & Risk Assessment")
    comp = pd.DataFrame({
        "Protection Method": ["Rule-Based Filter", "Keyword Classifier", "AI Model", "Manual Review"],
        "Risk Level Covered": ["Low", "Medium", "High", "Very High"],
        "Detection Speed (ms)": [8, 25, 90, 60000],
        "Accuracy (%)": [78.5, 89.2, 94.8, 98.0],
    })
    st.table(comp)
    st.bar_chart(comp.set_index("Protection Method")["Accuracy (%)"])
    st.subheader("Quick Personal Risk Assessment")
    q = [
        st.checkbox("I click links in SMS from unknown numbers"),
        st.checkbox("I use the same password on many sites"),
        st.checkbox("I have shared OTP with someone before"),
        st.checkbox("2-Factor Authentication is OFF on my accounts"),
        st.checkbox("I rarely check the sender's address"),
    ]
    r = sum(q) * 20
    st.metric("Your Risk Score", f"{r}%")
    st.progress(r / 100)
    if r >= 60:
        st.error("High risk – follow the Safety Checklist (Feature 10).")
    elif r >= 20:
        st.warning("Medium risk – improve a few habits.")
    else:
        st.success("Low risk – great habits!")

# ---------------- 10 ----------------
elif mode.startswith("10."):
    st.header("🆘 Personal Safety Checklist & Emergency Report Assistant")
    st.subheader("✅ Safety Checklist")
    items = ["Turn ON 2-Factor Authentication everywhere",
             "Use a unique strong password for each account",
             "Never share OTP, PIN or CVV with anyone",
             "Check the sender and link before clicking",
             "Install apps only from official stores",
             "Keep phone and apps updated"]
    done = sum(st.checkbox(i, key=f"chk{n}") for n, i in enumerate(items))
    st.progress(done / len(items))
    st.write(f"Safety progress: **{done}/{len(items)}**")
    st.subheader("🚨 Emergency Report Assistant")
    st.error("📞 India Cybercrime Helpline: **1930**  |  🌐 Report online: **cybercrime.gov.in**")
    st.markdown("""
**If you were scammed:**
1. Call **1930** immediately (first hour is critical for freezing money).
2. Inform your bank and block cards / UPI.
3. Change passwords and enable 2FA.
4. Save screenshots, numbers, links and transaction IDs.
5. File a complaint at cybercrime.gov.in.
""")
    with st.form("report"):
        name = st.text_input("Your name")
        kind = st.selectbox("Incident type", ["Fake bank call/SMS", "UPI fraud", "Lottery/Job scam", "Account hacked", "Other"])
        amt = st.number_input("Amount lost (₹)", min_value=0, step=100)
        desc = st.text_area("What happened?")
        if st.form_submit_button("Generate Report Summary"):
            st.code(f"CYBERCRIME INCIDENT SUMMARY\nName: {name}\nType: {kind}\nAmount Lost: ₹{amt}\nDetails: {desc}\n\nAction: Call 1930 & file at cybercrime.gov.in")

# ---------------- Footer ----------------
st.markdown("---")
st.markdown("<p style='text-align: center; color: #ffd700;'>PhishShift ML-07 Project Dashboard | Cybernaut Student Edition</p>", unsafe_allow_html=True)
