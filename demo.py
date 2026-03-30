import os
import requests
import json
from openai import OpenAI

# Agent configuration
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

ENV_URL = "http://localhost:7860"

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=OPENAI_API_KEY
)

DEMO_CASES = [
    {
        "id": 21,
        "name": "🍕 The Pizza Party (Fake Urgency Trap)",
        "description": "Uses 'ASAP' and 'IMMEDIATELY' for a non-urgent social event."
    },
    {
        "id": 22,
        "name": "🔥 The Polite Crisis (DevOps Outage Trap)",
        "description": "Describes a silent production failure in a calm, professional tone."
    },
    {
        "id": 23,
        "name": "🛡️ The Deceptive Phish (Security Alert Trap)",
        "description": "Mimics a security alert to test if the agent misidentifies sophisticated spam."
    }
]

def run_demo_case(case):
    print(f"\n🚀 SHOWNING DRAMATIC DEMO: {case['name']}")
    print(f"Goal: {case['description']}")
    
    # 1. Reset for specific ID
    try:
        response = requests.get(f"{ENV_URL}/reset?email_id={case['id']}")
        obs = response.json()
    except Exception as e:
        print(f"Error: Could not connect to environment. Is main.py running? ({e})")
        return

    print(f"\n📥 INBOX RECEIVED:")
    print(f"\"{obs['email_text']}\"")
    print(f"Urgency Score: {obs['urgency']}")

    # 2. Agent Reasoning
    prompt = f"""
    You are an AI Email Assistant. Analyze this email.
    Text: "{obs['email_text']}"
    Urgency Score: {obs['urgency']}

    Decide category (spam, urgent, normal), priority (low, medium, high), and response.
    Return JSON: {{"category": "...", "priority": "...", "response": "...", "strategic_priority": 0.5}}
    """

    print("\n🤖 AGENT IS ANALYZING...")
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    action = json.loads(completion.choices[0].message.content)
    print(f"Agent Action: {action['category'].upper()}, {action['priority'].upper()}")
    
    # 3. Score
    result = requests.post(f"{ENV_URL}/step", json=action).json()
    score = result['info']['score']
    mistake = result['info'].get('mistake')
    
    if score >= 0.8:
        print(f"\n✅ VERDICT: PASS")
        print(f"The agent demonstrated true contextual intelligence (Score: {score})")
    else:
        print(f"\n❌ VERDICT: FAIL")
        print(f"The agent was misled by surface-level signals (Score: {score})")
        if mistake:
            print(f"Technical Introspection: {mistake}")

if __name__ == "__main__":
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY environment variable is not set.")
    else:
        print("====================================================")
        print("   OPENENV EMAIL TRIAGE: ADVERSARIAL SHOWDOWN       ")
        print("====================================================")
        for case in DEMO_CASES:
            run_demo_case(case)
            print("-" * 52)
