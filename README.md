# 🔧 VibeFix AI – Smart Fundi Matcher Chatbot

VibeFix AI is an intelligent assistant that connects users with reliable local *fundis* (technicians and freelancers) in Kenya. Users simply type in natural language requests like:

> "I need a plumber in Githurai"

The AI extracts the *service* and *location*, then returns a matching fundi's details (name, skill, phone, WhatsApp link).

---

## 🚀 Features

✅ Natural language input (English/Kenyan context)  
✅ AI-powered skill & location extraction (via OpenRouter / GPT)  
✅ Matches user to local fundis in a CSV or Google Sheet  
✅ FastAPI backend with optional Streamlit frontend  
✅ Fully offline-ready with local CSV file  
✅ Easy to expand to WhatsApp, Glide, or mobile app

---

## 🧠 Tech Stack

| Component       | Technology           |
|----------------|----------------------|
| Language Model  | OpenRouter (Mistral or GPT)  
| Backend API     | FastAPI  
| Frontend (Optional) | Streamlit  
| Data Storage    | CSV file (fundis.csv)  
| Matching Logic  | GPT-based prompt extraction + Pandas filtering

---

## 🗂 Project Structure
