import streamlit as st
st.set_page_config(page_title="AI Email Generator", layout="wide")
st.sidebar.markdown(
    """
    <style>
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .sidebar-banner {
        background: linear-gradient(135deg, #0F0C29, #302B63, #000000);
        background-size: 400% 400%;
        animation: gradientMove 12s ease infinite;
        width: 100%;
        padding: 10px 12px;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
        text-align: center;
        color: white;
        font-size: 18px;
        font-weight: bold;
        font-family: Georgia, serif;
        margin-bottom: 15px;
        word-wrap: break-word;
    }
    </style>
    <div class="sidebar-banner">
        Generate and Send Emails Effortlessly
    </div>
    """, unsafe_allow_html=True
)

st.markdown("""
    <style>
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .banner {
        background: linear-gradient(135deg, #0F0C29, #302B63, #000000);
        background-size: 400% 400%;
        animation: gradientMove 12s ease infinite;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
        color: white;
        font-weight: bold;
        font-size: 32px;
        font-family: 'Segoe UI', sans-serif;
        margin-bottom: 20px;
    }
    </style>
    <div class="banner">
        AI-Powered Email Assistant
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .subheader{
        text-align: center;
        color: white;
        font-weight: bold;
        font-size: 18px;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
    <div class="subheader">
        Generate professional emails instantly, tailored to your needs
    </div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
left, center, right = st.columns([1, 2, 1])
with center:
    with st.form("email_form"):
        subject = st.text_input("Enter the Email subject", placeholder="E.g., Meeting Follow-Up, Project Update, etc.")
        tone = st.selectbox("Select the tone of the email", ["Formal", "Informal", "Friendly", "Professional", "Casual"])
        key_points = st.text_area("Provide key points or details", placeholder="E.g., Meeting date, project details, recipient's name, etc.", height=150)
        senders_email = st.text_input(
            "Enter your email address", 
            placeholder="E.g., jack1234@gmail.com",
            help="We'll use this email to send the generated email.")
        recipient_email = st.text_input(
            "Enter recipient's email address", 
            placeholder="E.g., sarah1234@gmail.com"
        )
        recipient_name = st.text_input("Enter the recipient's name", placeholder="E.g., John, Sarah, etc.")
        sender_name = st.text_input("Enter your name", placeholder="E.g., Alex, Emily, etc.")
        button = st.form_submit_button("Generate Email")
if button:
    if not senders_email or not senders_email.lower().endswith("@gmail.com"):
        st.error("⚠️ Please enter a valid Gmail address for the sender.")
    elif not recipient_email or not recipient_email.lower().endswith("@gmail.com"):
        st.error("⚠️ Please enter a valid Gmail address for the sender.")
    st.success("✅ Both email addresses are valid! Proceeding...")
    st.session_state["senders_email"] = senders_email
    st.session_state["recipient_email"] = recipient_email
    st.session_state["subject"] = subject
    st.session_state["tone"] = tone
    st.session_state["key_points"] = key_points
    st.session_state["recipient_name"] = recipient_name
    st.session_state["sender_name"] = sender_name
    st.switch_page("pages/Email.py")
