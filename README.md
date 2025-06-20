# 🌿 Wellness-AI: Your Personal Wellness and Therapy Assistant

Wellness-AI is a Streamlit-based web application designed to support users in their mental wellness journey. It offers an AI-powered therapy chatbot, mood and journal tracking, affirmations, goal management, and personalized analytics — all in one place.

---

## 🧠 Features

### 🔐 Authentication System
- Email-based OTP verification for signup and password reset
- Secure login with user session handling
- User profile with editable personal and medical info

### 💬 AI Therapy Chat
- Interactive chatbot trained to be an empathetic listener
- Generates helpful, kind responses and follow-up questions
- Powered by OpenRouter + OpenAI models (e.g., Mistral-7B)

### 😊 Mood Tracker
- Log daily mood in one click
- Stores data in CSV format for visualization

### 📘 Sentiment Journal
- Journal with automatic sentiment analysis (Positive, Negative, Neutral)
- Saves entries with analysis explanation
- Visualized in analytics

### 🚧 Goal Tracker
- Set and manage personal goals (e.g., fitness, sleep, mindfulness)
- Data stored in `goals.csv`

### 📊 Analytics Dashboard
- Mood trend graphs
- Sentiment bar charts from journal entries

### 🌞 Daily Affirmations
- Gentle, rotating affirmations for encouragement

### 👤 User Profile
- Displays name, email, blood group, and medical history
- Profile photo and editable medical history section

---

## 📁 Project Structure

```bash
Wellness_AI/
│
├── app.py                  # Main Streamlit application
├── goal_tracker.py         # Logic for goal management page
├── users.json              # User database (email, password, etc.)
├── mood_log.csv            # Mood tracker data
├── journal_log.csv         # Journal and sentiment data
├── goals.csv               # User goals data
├── .env                    # Stores API keys and email credentials
└── requirements.txt        # Python dependencies
