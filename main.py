from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.env import EmailEnv
from app.models import Action, Observation, Reward
from typing import Dict, Any

app = FastAPI(title="OpenEnv Email Triage Assistant")

# Initialize environment
env = EmailEnv()

@app.get("/reset")
def reset(task: str = "full", email_id: int = None):
    """
    Resets the environment and returns the initial observation.
    Supports selecting a specific email ID for testing/demo.
    """
    obs = env.reset(task=task, email_id=email_id)
    return obs

@app.post("/step")
def step(action: Action):
    """
    Takes an action and returns the next observation, reward, and done status.
    """
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    """
    Returns the current internal state of the environment.
    """
    return env.state()

# Serve frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def read_index():
    """
    Serves the main dashboard UI.
    """
    return FileResponse("frontend/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
