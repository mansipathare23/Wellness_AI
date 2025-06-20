# app.py

# ------------ Import Required Libraries ------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import random
import json
import secrets
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from openai import OpenAI
from goal_tracker import goal_tracker_page


# ------------ Load Environment Variables (.env file) ------------
load_dotenv()

# ------------ OpenAI API Client Setup ------------
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# ------------ Email Configuration ------------
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
USER_FILE = "users.json"

# ------------ Load Existing Users from File ------------
def load_users():
    if not os.path.exists(USER_FILE):
        return []
    with open(USER_FILE, "r") as f:
        return json.load(f)

# ------------ Save Users to File ------------
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

# ------------ Generate 6-digit OTP ------------
def generate_otp():
    return str(secrets.randbelow(900000) + 100000)

# ------------ Send OTP to Email for Signup/Reset ------------
def send_email_otp(email, otp):
    try:
        msg = EmailMessage()
        msg.set_content(f"Your OTP for Wellness-AI is: {otp}")
        msg["Subject"] = "Wellness-AI Email OTP Verification"
        msg["From"] = EMAIL_USER
        msg["To"] = email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# ------------ Streamlit App Configuration ------------
st.set_page_config(page_title="Wellness-AI", layout="centered")

# ------------ Session State Initialization ------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.current_user = None
    st.session_state.email_otp = None
    st.session_state.forgot_password = False

# ------------ SIDEBAR (Visible Only Before Login) ------------
if not st.session_state.authenticated:
    st.sidebar.title("🌿 Wellness-AI")
    st.sidebar.markdown("___")
    st.sidebar.markdown("### 🌞 Welcome to Your Wellness Hub")
    st.sidebar.markdown("#### 🚀 What You Can Do:")
    st.sidebar.markdown("""
    - 🧠 Log your emotions  
    - ✍️ Journal with reflection  
    - 💬 Talk to your AI life coach  
    - 📊 Visualize your wellness trends  
    - 🌸 Receive gentle affirmations  
    """)
    st.sidebar.image(
    "https://images.pexels.com/photos/3822622/pexels-photo-3822622.jpeg",
    caption="🌿 Embrace calmness. You are in a safe space.",
    use_container_width=True
    )

    st.sidebar.markdown("#### 💡 Today's Reminder")
    st.sidebar.markdown(
        "> _“You don’t have to control your thoughts. You just have to stop letting them control you.”_"
    )
    st.sidebar.markdown("___")
    st.sidebar.markdown("🌸 Be gentle with yourself • 🌈 You’re growing every day • 🧘 Take one mindful step at a time")

# ------------ FRONT PAGE - LOGIN/SIGNUP/RESET PASSWORD ------------

# ----- Show Reset Password Page -----
if not st.session_state.authenticated and st.session_state.forgot_password:
    st.subheader("🔁 Reset Password")

    if "reset_email" not in st.session_state:
        st.session_state.reset_email = ""

    st.text_input("Registered Email", key="reset_email")

    if st.button("Send Reset OTP"):
        users = load_users()
        if any(u["email"] == st.session_state.reset_email for u in users):
            otp = generate_otp()
            st.session_state.email_otp = otp
            if send_email_otp(st.session_state.reset_email, otp):
                st.success("OTP sent to registered email!")
        else:
            st.error("Email not registered.")

    st.text_input("Enter OTP", key="reset_otp")
    st.text_input("New Password", type="password", key="new_pass")

    if st.button("Reset Now"):
        if st.session_state.reset_otp == st.session_state.get("email_otp"):
            users = load_users()
            for u in users:
                if u["email"] == st.session_state.reset_email:
                    u["password"] = st.session_state.new_pass
                    save_users(users)
                    st.success("Password reset successful!")
                    st.session_state.email_otp = None
                    st.session_state.forgot_password = False
                    st.rerun()
                    break
        else:
            st.error("Incorrect OTP.")

    if st.button("← Back"):
        st.session_state.forgot_password = False
        st.rerun()

# ----- Show Login and Signup Tabs -----
elif not st.session_state.authenticated:
    tab1, tab2 = st.tabs(["🔐 Login", "📩 Signup"])

    # ----- Login Tab -----
    with tab1:
        st.subheader("🔐 Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            users = load_users()
            user = next((u for u in users if u["email"] == email and u["password"] == password and u.get("verified")), None)
            if user:
                st.session_state.authenticated = True
                st.session_state.current_user = email
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials or account not verified.")

        if st.button("Forgot Password?"):
            st.session_state.forgot_password = True
            st.rerun()

    # ----- Signup Tab -----
    with tab2:
        st.subheader("📩 Signup")

        if "signup_name" not in st.session_state: st.session_state.signup_name = ""
        if "signup_email" not in st.session_state: st.session_state.signup_email = ""
        if "signup_password" not in st.session_state: st.session_state.signup_password = ""
        if "signup_otp" not in st.session_state: st.session_state.signup_otp = ""

        name = st.text_input("Name", key="signup_name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")

        if st.button("Send OTP"):
            users = load_users()
            if any(u["email"] == email for u in users):
                st.warning("Account already exists.")
            else:
                otp = generate_otp()
                st.session_state.email_otp = otp
                st.session_state.pending_user = {"name": name, "email": email, "password": password}
                if send_email_otp(email, otp):
                    st.success("OTP sent to your email!")

        st.text_input("Enter OTP to verify", key="signup_otp")
        if st.button("Create Account"):
            if st.session_state.signup_otp == st.session_state.get("email_otp"):
                users = load_users()
                user = st.session_state.pending_user
                user["verified"] = True
                users.append(user)
                save_users(users)
                st.success("Account created successfully! Please login.")

                # Clear signup data
                st.session_state.signup_name = ""
                st.session_state.signup_email = ""
                st.session_state.signup_password = ""
                st.session_state.signup_otp = ""
                st.session_state.email_otp = None
                st.session_state.pending_user = None
            else:
                st.error("Invalid OTP!")

    # Stop here if not logged in
    st.stop()

# ------------ MAIN DASHBOARD (After Login) ------------
# Sidebar Navigation after login
page = st.sidebar.radio("Go to", [
    "Home",
    "Chat with AI",
    "Mood Tracker",
    "Analytics",
    "Goal Tracker",
    "Affirmations",
    "Journal with Sentiment"
])

# ------------ HOME PAGE ------------
if page == "Home":
    st.title("🌿 Welcome to Wellness-AI")
    st.markdown("Your personal AI-powered wellness and therapy assistant.")
    st.image("https://images.unsplash.com/photo-1503676260728-1c00da094a0b", use_container_width=True)

# ------------ (Other pages like Chat, Mood Tracker etc. can follow here) ------------


# ------------------ CHAT PAGE ------------------ #
elif page == "Chat with AI":
    st.title("💬 Talk to Your AI Therapy Bot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "system", "content": "You are a friendly and empathetic therapy assistant."}
        ]

    for msg in st.session_state.chat_history[1:]:
        st.markdown(f"🧑‍💬 **You**: {msg['content']}" if msg["role"] == "user" else f"🤖 **Therapist**: {msg['content']}")

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message", key="user_input_chat")
        submitted = st.form_submit_button("Send")

    if submitted and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("AI is responding..."):
            try:
                response = client.chat.completions.create(
                    model="mistralai/mistral-7b-instruct",
                    messages=st.session_state.chat_history,
                    max_tokens=512
                )
                reply = response.choices[0].message.content.strip()
                st.session_state.chat_history.append({"role": "assistant", "content": reply})

                follow_up_prompt = {
                    "role": "user",
                    "content": "Can you ask me a follow-up question to continue our therapy conversation?"
                }
                follow_up = client.chat.completions.create(
                    model="mistralai/mistral-7b-instruct",
                    messages=st.session_state.chat_history + [follow_up_prompt],
                    max_tokens=256
                )
                follow_up_question = follow_up.choices[0].message.content.strip()
                st.session_state.chat_history.append({"role": "assistant", "content": follow_up_question})
            except Exception as e:
                st.error(f"Error: {e}")

# ------------------ MOOD TRACKER ------------------ #
elif page == "Mood Tracker":
    st.title("😊 Mood Tracker")
    mood = st.radio("How do you feel today?", ["😊 Happy", "😐 Neutral", "😢 Sad", "😰 Anxious", "😠 Angry"])
    if st.button("Log Mood"):
        if not os.path.exists("mood_log.csv"):
            df = pd.DataFrame(columns=["date", "mood"])
            df.to_csv("mood_log.csv", index=False)
        df = pd.read_csv("mood_log.csv")
        new_entry = {"date": datetime.now(), "mood": mood}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv("mood_log.csv", index=False)
        st.success("Mood logged!")

# ------------------ ANALYTICS ------------------ #
elif page == "Analytics":
    st.title("📊 Mood Analytics")

    if os.path.exists("mood_log.csv"):
        df = pd.read_csv("mood_log.csv")
        df['date'] = pd.to_datetime(df['date'])
        mood_counts = df.groupby([df['date'].dt.date, 'mood']).size().unstack().fillna(0)
        st.subheader("📈 Mood Trends")
        st.line_chart(mood_counts)

    if os.path.exists("journal_log.csv"):
        st.subheader("📘 Journal Sentiment Trends")
        jdf = pd.read_csv("journal_log.csv")
        jdf['date'] = pd.to_datetime(jdf['date'])
        sentiment_counts = jdf.groupby([jdf['date'].dt.date, 'sentiment']).size().unstack().fillna(0)
        st.bar_chart(sentiment_counts)

# ------------------ GOAL TRACKER ------------------ #
elif page == "Goal Tracker":
    goal_tracker_page()


# ------------------ AFFIRMATIONS ------------------ #
elif page == "Affirmations":
    st.title("🌞 Daily Affirmation")
    affirmations = [
        "You are capable of amazing things.",
        "Each day is a fresh start.",
        "You deserve to feel good about yourself.",
        "Breathe in peace, breathe out stress.",
        "You are enough just as you are."
    ]
    st.markdown("✨ **" + random.choice(affirmations) + "** ✨")

# ------------------ JOURNAL WITH SENTIMENT ------------------ #
elif page == "Journal with Sentiment":
    st.title("📝 Daily Journal with Sentiment Analysis")
    journal_entry = st.text_area("Write about your day", height=200)
    analyze = st.button("Analyze & Save Entry")

    if analyze and journal_entry.strip():
        try:
            with st.spinner("Analyzing your entry..."):
                prompt = f"""Analyze the emotional sentiment of this journal entry. Classify it as Positive, Negative, or Neutral. Also explain the reason:\n{journal_entry}"""

                response = client.chat.completions.create(
                    model="mistralai/mistral-7b-instruct",
                    messages=[
                        {"role": "system", "content": "You are a sentiment analysis assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=512
                )
                result = response.choices[0].message.content.strip()

                sentiment = "Neutral"
                if "Positive" in result:
                    sentiment = "Positive"
                elif "Negative" in result:
                    sentiment = "Negative"

                log_file = "journal_log.csv"
                if not os.path.exists(log_file):
                    df = pd.DataFrame(columns=["date", "entry", "sentiment", "analysis"])
                    df.to_csv(log_file, index=False)

                df = pd.read_csv(log_file)
                new_entry = {
                    "date": datetime.now(),
                    "entry": journal_entry,
                    "sentiment": sentiment,
                    "analysis": result
                }
                df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
                df.to_csv(log_file, index=False)

                st.success(f"Sentiment: **{sentiment}**")
                st.info(result)
        except Exception as e:
            st.error("Something went wrong. Please check your connection or API key.")
