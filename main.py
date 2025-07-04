
# importing necessary libraries
from fastapi import FastAPI, Request
import pandas as pd
import requests

# Load fundi dataframe
df = pd.read_csv("fundis.csv") 

# Your OpenRouter API key
OPENROUTER_API_KEY = "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" 

app = FastAPI()

def generate_prompt(user_request):
    return f"""
You are a smart assistant that helps clients find the right fundi (technician or freelancer) in Kenya.
The client says: \"{user_request}\"
Extract:
Skill: [e.g., plumber]
Location: [e.g., Githurai]
"""

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
    json_response = response.json()

    if "choices" not in json_response:
        print("❌ OpenRouter Error:", json_response)
        return None, None

    content = json_response["choices"][0]["message"]["content"]
    skill, location = None, None
    for line in content.splitlines():
        if "Skill:" in line:
            skill = line.split(":")[1].strip().lower()
        elif "Location:" in line:
            location = line.split(":")[1].strip().lower()
    return skill, location

def match_fundi(skill, location):
    result = df[
        (df['Skill'].str.lower() == skill) &
        (df['Location'].str.lower() == location)
    ]
    if result.empty:
        return {"message": "❌ No fundi found for that skill and location."}
    fundi = result.iloc[0]
    return {
        "name": fundi['Name'],
        "skill": fundi['Skill'],
        "location": fundi['Location'],
        "phone": fundi['Phone'],
        "whatsapp": fundi['WhatsApp_Link']
    }

@app.post("/match")
async def get_fundi(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    skill, location = extract_job_info(user_input)
    if not skill or not location:
        return {"error": "Could not extract skill or location."}
    return match_fundi(skill, location)
