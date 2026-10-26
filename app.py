import streamlit as st
import pandas as pd
import re
from datetime import datetime
from urllib.parse import urlparse

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="PhishShift Safety Hub",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- BLACK & GOLD THEME ----------------
st.markdown("""
<style>
.stApp {
    background-color: #080808;
    color: #f5f5f5;
}
[data-testid="stSidebar"] {
    background-color: #111111;
}
h1, h2, h3 {
    color: #FFD700 !important;
}
.stButton > button {
    background: linear-gradient(135deg, #FFD700, #B8860B);
    color: black;
    font-weight: bold;
    border-radius: 8px;
    border: none;
    min-height: 42px;
}
.stTextArea textarea, .stTextInput input {
    background-color: #171717 !important;
    color: white !important;
    border: 1px solid #B8860B !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION DATA ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- MESSAGE CHECKER ----------------
def check_message(message):
    text = message.lower()

    patterns = {
        "Urgent action requested": [
            "urgent", "immediately", "act now", "expires today"
        ],
        "Account or password details requested": [
            "password", "otp", "pin", "verify your account",
            "account locked", "kyc update"
        ],
        "Unexpected prize or money offer": [
            "you won", "free prize", "claim reward",
            "lottery winner", "free money"
        ],
        "Suspicious link language": [
            "click here", "verify now", "login here",
            "update your details"
        ]
    }

    found = []

    for category, keywords in patterns.items():
        matches = [word for word in keywords if word in text]

        if matches:
            found.append({
                "Warning": category,
                "Matched words": ", ".join(matches)
            })

    return found

# ---------------- WEBSITE CHECKER ----------------
def check_website(link):
    link = link.strip()

    if not link:
        return ["Please enter a website address."]

    candidate = link if "://" in link else "https://" + link
    parsed = urlparse(candidate)
    host = (parsed.hostname or "").lower()
    warnings = []

    if not host or "." not in host:
        warnings.append("The website address looks incomplete.")

    if parsed.scheme.lower() == "http":
        warnings.append("This website uses HTTP instead of HTTPS.")

    if "@" in parsed.netloc:
        warnings.append("The address contains an unusual @ symbol.")

    if len(host) > 45:
        warnings.append("The website address is unusually long.")

    if host.count("-") >= 3:
        warnings.append("The address contains several hyphens.")

    if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", host):
        warnings.append("The address uses a numeric IP address.")

    if not warnings:
        warnings.append(
            "No basic warning signs found. The website is not guaranteed safe."
        )

    return warnings

# ---------------- SAVE RECENT CHECK ----------------
def save_check(item, result):
    st.session_state.history.insert(0, {
        "Time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "Checked Item": item[:100],
        "Result": result
    })

    st.session_state.history = st.session_state.history[:50]

# ---------------- SIDEBAR ----------------
st.sidebar.title("🛡️ PhishShift")
st.sidebar.write("Your Online Safety Assistant")

page = st.sidebar.radio(
    "Choose a page",
    [
        "Home Dashboard",
        "Check a Message",
        "Check a Website",
        "Scam Alerts & Safety Tips"
    ]
)

# ---------------- HOME DASHBOARD ----------------
if page == "Home Dashboard":

    st.title("🛡️ PhishShift Safety Hub")
    st.subheader("Stay alert. Stay safe online.")

    st.write(
        "Check suspicious messages and website addresses. "
        "Learn how to recognise common scams and protect your information."
    )

    total_checks = len(st.session_state.history)

    col1, col2 = st.columns(2)

    col1.metric("Total Checks", total_checks)
    col2.metric("Safety Tools", 3)

    st.markdown("### What would you like to check?")

    col1, col2 = st.columns(2)

    with col1:
        st.info("📩 **Message Safety**")
        st.write("Check an email or SMS for common scam warning signs.")

    with col2:
        st.info("🔗 **Website Safety**")
        st.write("Look for common warning signs in a website address.")

    st.markdown("### Important Safety Reminder")

    st.warning(
        "Never share your password, bank PIN, or OTP with anyone. "
        "Verify urgent requests through an official contact method."
    )

    st.caption(
        "PhishShift provides basic checks and cannot guarantee that "
        "a message or website is safe."
    )

# ---------------- CHECK A MESSAGE ----------------
elif page == "Check a Message":

    st.title("📩 Check a Message")

    st.write(
        "Paste a suspicious SMS, email, or chat message below."
    )

    message = st.text_area(
        "Your message",
        placeholder="Paste the message here...",
        height=150
    )

    if st.button("Check Message"):

        if not message.strip():
            st.warning("Please enter a message first.")

        else:
            results = check_message(message)

            if results:
                st.error("Possible scam warning signs found.")

                for result in results:
                    st.write("⚠️", result["Warning"])
                    st.caption(
                        "Matched text: " + result["Matched words"]
                    )

                st.markdown("### What should you do?")

                st.write("- Do not click unexpected links.")
                st.write("- Never share passwords or OTPs.")
                st.write("- Verify the sender independently.")
                st.write("- Contact your bank through official channels if needed.")

                save_check(message, "Warning signs found")

            else:
                st.success("No configured warning signs were found.")

                st.info(
                    "This does not prove the message is genuine. "
                    "Check the sender and verify important requests."
                )

                save_check(message, "No basic warning signs")

# ---------------- CHECK A WEBSITE ----------------
elif page == "Check a Website":

    st.title("🔗 Check a Website")

    st.write(
        "Enter a website address to check for some common warning signs. "
        "This tool does not open the website."
    )

    link = st.text_input(
        "Website address",
        placeholder="https://example.com"
    )

    if st.button("Check Website"):

        if not link.strip():
            st.warning("Please enter a website address.")

        else:
            results = check_website(link)

            for result in results:
                st.warning("⚠️ " + result)

            st.info(
                "This is a basic address check only. A dangerous website "
                "may have no obvious warning signs."
            )

            save_check(link, "Website address checked")

# ---------------- SCAM ALERTS & SAFETY TIPS ----------------
elif page == "Scam Alerts & Safety Tips":

    st.title("🚨 Scam Alerts & Safety Tips")

    with st.expander("📱 Fake bank messages"):
        st.write(
            "A message may claim your bank account will be blocked. "
            "Check directly with your bank using its official app or phone number."
        )

    with st.expander("🎁 Prize and reward scams"):
        st.write(
            "Be careful with unexpected prizes that ask for money "
            "or personal information before you can claim them."
        )

    with st.expander("🔐 Password and OTP scams"):
        st.write(
            "Never share passwords, OTPs, PINs, or account recovery codes."
        )

    with st.expander("🎙️ Voice and impersonation scams"):
        st.write(
            "A caller may pretend to be a family member or an official. "
            "Verify their identity through another trusted contact method."
        )

    with st.expander("🔗 Suspicious website links"):
        st.write(
            "Check the domain carefully. Avoid entering personal information "
            "on a site reached through an unexpected message."
        )

    st.markdown("### Your Safety Checklist")

    st.checkbox("I check the sender before responding.")
    st.checkbox("I avoid unexpected links and attachments.")
    st.checkbox("I never share my password or OTP.")
    st.checkbox("I verify urgent payment requests independently.")

    st.divider()

    st.markdown("### Need to Report a Scam?")

    st.write(
        "In India, suspected financial cybercrime can be reported "
        "through the national cybercrime helpline 1930 or the official "
        "cybercrime reporting portal."
    )

# ---------------- FOOTER ----------------
st.divider()

st.markdown(
    "<p style='text-align:center;color:#FFD700;'>"
    "PhishShift | Online Safety Assistant"
    "</p>",
    unsafe_allow_html=True
)
