import streamlit as st
import requests
import json
import PyPDF2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
        View and Send Generated Emails
    </div>
    """, unsafe_allow_html=True
)
PORT = st.secrets["PORT"]
HOST = st.secrets["HOST"]
API_KEY = st.secrets["API_KEY"]
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
        Generated Email Preview & Sender
    </div>
""", unsafe_allow_html=True)
st.markdown("""
        <style>
        .subheader{
            text-align: center;
            color: white;
            font-weight: bold;
            font-size: 24px;
            font-family: 'Segoe UI', sans-serif;
        }
        </style>
        <div class="subheader">
        Here are the details of your generated email
        </div>
    """, unsafe_allow_html=True)
if 'processing' not in st.session_state:
    st.session_state.processing = False
recipient_email = st.session_state.get('recipient_email', '')
senders_email = st.session_state.get('senders_email', '')
# st.markdown("### Here are the details you provided:")
if all(key in st.session_state for key in ['subject', 'tone', 'key_points', 'recipient_name', 'sender_name']):
    subject = st.session_state['subject']
    tone = st.session_state['tone']
    key_points = st.session_state['key_points']
    sender_name = st.session_state['sender_name']
    recipient_name = st.session_state['recipient_name']
    st.markdown("### Here are the details you provided:")
    st.markdown(f"- **Email Subject:** {subject}")
    st.markdown(f"- **Tone:** {tone}")
    st.markdown(f"- **Key Points:** {key_points}")
    st.markdown(f"- **Recipient's Name:** {recipient_name}")
    st.markdown(f"- **Sender's Name:** {sender_name}")
    if senders_email:
        st.markdown(f"- **Sender's Email:** {senders_email}")
    if recipient_email:
        st.markdown(f"- **Recipient's Email:** {recipient_email}")
    st.markdown("---")
    file_upload = st.radio("Would you like to upload a PDF file to extract additional details for the email? (Optional)", ("Yes", "No"), index=1,help ="Uploading a PDF can help include more specific information in the generated email.")
    pdf_text = ""
    if file_upload == "Yes":
        st.info("Please Make sure your PDF is text-based for accurate extraction.")
        attach_file = st.file_uploader("Upload a PDF file to extract additional details", type=["pdf"],help ="The content from the PDF will be used to enhance the email generation.")
        if attach_file:
            try:
                st.spinner("Reading and extracting text from the PDF...")
                st.success("PDF file uploaded successfully!")
                pdf_render = PyPDF2.PdfReader(attach_file)
                for page in pdf_render.pages:
                    pdf_text += page.extract_text() or ""
            except Exception as e:
                st.error(f"Error reading PDF file: {e}")
        else:
            st.info("No PDF file uploaded. Proceeding without additional details.")
    st.markdown("### 📧 Generated Email:")
    if pdf_text:
        prompt = f"""
    Generate a {tone.lower()} email based on the following details:
    - Subject: {subject}
    - Key Points: {key_points}
    - Recipient's Name: {recipient_name}
    - Sender's Name: {sender_name}
    "Write a professional follow-up email. "
                        "The email must be a minimum of 3 paragraphs. "
                        "Ensure the email is well-structured with a subject line, greeting, introduction, body, and closing. "
                        "Keep the language clear, concise, and easy to read. "
                        "Use a friendly but professional tone throughout. "
                        "Summarize key discussion points, outline next steps, and end with a courteous closing."
    """ + f"Here are additional details from the attached PDF to include in the email: {pdf_text}"+f"Do not leave anything out from the PDF. Make sure to include all relevant information from the PDF in the email.if the information from the PDF contradicts the key points, prioritize the PDF information.if the inofrmation is not provided donot include the sentences in the email."
    else: 
        prompt = f"""
    Generate a {tone.lower()} email based on the following details:
    - Subject: {subject}
    - Key Points: {key_points}
    - Recipient's Name: {recipient_name}
    - Sender's Name: {sender_name}
    "Write a professional follow-up email. "
                        "The email must be a minimum of 3 paragraphs. "
                        "Ensure the email is well-structured with a subject line, greeting, introduction, body, and closing. "
                        "Keep the language clear, concise, and easy to read. "
                        "Use a friendly but professional tone throughout. "
                        "Summarize key discussion points, outline next steps, and end with a courteous closing."
    """+f"Do not leave anything out from the PDF. Make sure to include all relevant information from the PDF in the email.if the information from the PDF contradicts the key points, prioritize the PDF information.if the inofrmation is not provided donot include the sentences in the email."
    GEMINI_API_URL = st.secrets["GEMINI_API_URL"]
    if st.button("✉️ Generate Email"):
        with st.spinner("Generating your email..."):
            url = st.secrets["GEMINI_API_URL_INFERENCE"]
            headers = {
                "Content-Type": "application/json",
            }
            data = {
                "contents": [{
                "parts": [{"text": prompt}]
            }]
            }
            response = requests.post(
            f"{GEMINI_API_URL}?key={API_KEY}",
            headers=headers,
            data=json.dumps(data)
        )
            if response.status_code == 200:
                output = response.json()['candidates'][0]['content']['parts'][0]['text']
                st.session_state.generated_email = output
                st.markdown(f"""
                <div style="border: 2px solid #4CAF50; border-radius: 10px; padding: 20px; background-color: black; color: white">
                    {output.replace('\n', '<br>')}
                </div>
                """, unsafe_allow_html=True)
                st.success("Email generated successfully!")
            else:
                st.warning(f"⚠️ Error {response.status_code}: {response.text}")
else:
    st.warning("⚠️ No form data found. Please go back and submit the form first.")
    st.page_link("Form.py", label="🔙 Back to Form")
PORT = 587
smtp = smtplib.SMTP(HOST, PORT)
check_box = st.checkbox(
    "I want to send the generated email now", 
    help="Check this box if you want to send the email immediately after generation."
)
if check_box:
    st.info("PLease Make sure You have enabled 2-Step Verification and created an App Password in your Google Account settings.")
    password = st.text_input(
        "Enter your Gmail App Password", 
        type="password", 
        help="⚠️ Use a 16-digit Gmail App Password, not your normal Gmail password."
    )
    send_email_button = st.button("📤 Send Email")
    if send_email_button:
        if not senders_email or not recipient_email:
            st.error("⚠️ Please ensure both sender and recipient email addresses are provided.")
        elif not password:
            st.error("⚠️ Please enter your Gmail app password to send the email.")
        else:
            try:
                smtp = smtplib.SMTP(HOST, PORT)
                smtp.ehlo()
                smtp.starttls()
                smtp.login(senders_email, password)
                msg = MIMEMultipart()
                msg["From"] = senders_email
                msg["To"] = recipient_email
                msg["Subject"] = subject
                msg.attach(MIMEText(st.session_state.generated_email, "plain"))
                smtp.send_message(msg)
                smtp.quit()
                st.success("✅ Email sent successfully!")
            except Exception as e:
                st.error(f"⚠️ Failed to send email: {e}")
