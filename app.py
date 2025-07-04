import streamlit as st
import pandas as pd
import requests

# Load fundis.csv
df = pd.read_csv("fundis.csv")

# OpenRouter API Key
OPENROUTER_API_KEY = "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" 

# Generate the prompt for GPT
def generate_prompt(user_request):
    return f"""
You are a smart assistant that helps clients find the right fundi (technician or freelancer) in Kenya.
The client says: "{user_request}"
Extract:
Skill: [e.g., plumber]
Location: [e.g., Githurai]
"""

# Call OpenRouter
def extract_job_info(user_request):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://chat.openai.com",
        "Content-Type": "application/json"
    }
    body = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": generate_prompt(user_request)}
        ]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
    result = response.json()
    
    if "choices" not in result:
        st.error(f"❌ OpenRouter error: {result}")
        return None, None

    content = result["choices"][0]["message"]["content"]

    # 🧠 Add this debug print
    st.code(content, language='text')

    skill, location = None, None
    for line in content.splitlines():
        if "Skill:" in line:
            skill = line.split(":")[1].strip().lower()
        elif "Location:" in line:
            location = line.split(":")[1].strip().lower()
    return skill, location

# Match fundi from DataFrame
def match_fundi(skill, location):
    result = df[
        (df['Skill'].str.lower() == skill) &
        (df['Location'].str.lower() == location)
    ]
    if result.empty:
        return None
    return result.iloc[0]

# Streamlit UI
st.title("🔧 VibeFix AI – Fundi Matcher")
st.write("Type your request below (e.g., *I need a painter in Umoja*)")

user_input = st.text_input("Your Request")

if user_input:
    with st.spinner("Thinking..."):
        skill, location = extract_job_info(user_input)
        if skill and location:
            fundi = match_fundi(skill, location)
            if fundi is not None:
                st.success("✅ Fundi Found!")
                st.markdown(f"**Name**: {fundi['Name']}")
                st.markdown(f"**Skill**: {fundi['Skill']}")
                st.markdown(f"**Location**: {fundi['Location']}")
                st.markdown(f"**Phone**: {fundi['Phone']}")
                st.markdown(f"[📱 WhatsApp Link]({fundi['WhatsApp_Link']})", unsafe_allow_html=True)
            else:
                st.error("❌ No fundi found for that skill and location.")
        else:
            st.warning("⚠️ Could not understand your request. Try again.")
