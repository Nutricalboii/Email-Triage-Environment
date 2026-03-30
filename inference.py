import os
import requests
import json
from openai import OpenAI
from pydantic import ValidationError

# Configuration from environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Local environment URL
ENV_URL = "http://localhost:7860"

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=OPENAI_API_KEY
)

def solve_email(task="full"):
    """
    Runs a single step of the environment using the LLM agent.
    """
    print(f"\n--- Starting Task: {task} ---")
    
    # 1. Reset environment
    try:
        response = requests.get(f"{ENV_URL}/reset?task={task}")
        obs = response.json()
    except Exception as e:
        print(f"Error resetting environment: {e}")
        return

    print(f"Email Received: {obs['email_text']}")
    print(f"Gravity (Urgency): {obs['gravity']}")

    # 2. Generate Action via LLM
    prompt = f"""
    You are an expert email triage assistant.
    Email: "{obs['email_text']}"
    Sender: {obs['sender']}
    Gravity (Urgency Score): {obs['gravity']}

    Task: {task}
    
    Instructions:
    1. Classify the email into one of these categories: spam, urgent, normal.
    2. Assign a priority: low, medium, high.
    3. Write a professional response (if it's not spam). Include relevant keywords.
    4. Set an 'antigravity' value (0.0 to 1.0). High gravity emails (urgent) should have low antigravity (0.1). Low gravity emails (spam/normal) can have high antigravity (0.9) to denote strategic delay.

    Return your answer EXACTLY in the following JSON format:
    {{
        "category": "spam|urgent|normal",
        "priority": "low|medium|high",
        "response": "Your response text here",
        "antigravity": 0.5
    }}
    """

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        action_data = json.loads(completion.choices[0].message.content)
        print(f"Agent Action: {json.dumps(action_data, indent=2)}")
        
        # 3. Take Step
        step_response = requests.post(f"{ENV_URL}/step", json=action_data)
        result = step_response.json()
        
        print(f"Reward: {result['reward']['score']}")
        print(f"Strategic Score: {result['info']['score']}")
        print(f"Done: {result['done']}")
        
        return result['info']['score']

    except Exception as e:
        print(f"Error during inference: {e}")
        return 0.0

if __name__ == "__main__":
    tasks = ["classification", "priority", "full"]
    total_score = 0
    
    for t in tasks:
        score = solve_email(t)
        total_score += score
    
    print(f"\nFinal Aggregate Score: {round(total_score / len(tasks), 2)}")
