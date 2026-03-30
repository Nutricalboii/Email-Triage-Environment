# OpenEnv Email Triage Assistant (with Antigravity UI) 📧

An industrial-grade, OpenEnv-compliant reinforcement learning environment for training and evaluating AI agents on real-world email triage tasks.

## 🚀 Overview

This environment simulates a professional inbox where an AI agent must handle incoming communications by classifying them, assigning priority, and generating appropriate responses. 

### ✨ The Antigravity Twist
Inspired by **Google Gravity**, the built-in dashboard features a physics-based "Falling UI" mode. It serves as a visual metaphor for the chaos of an unmanaged inbox—where urgency (gravity) pulls tasks down if not countered by strategic agent decisions (antigravity).

## 🛠️ Environment Specification (OpenEnv)

- **Observation Space**: Typed Pydantic models including `email_text`, `sender`, `gravity` (urgency), and `history`.
- **Action Space**: Enum-based categories (`spam`, `urgent`, `normal`), priorities (`low`, `medium`, `high`), and a `response` string.
- **Reward Function**: Programmatic scoring with partial rewards for correct classification, keyword matching, and strategic delay management.

### 🎮 Tasks & Difficulty
| Task ID | Level | Description |
|---------|-------|-------------|
| `classification` | Easy | Correctly identify the email category. |
| `priority` | Medium | Correctly assign priority levels to categorized emails. |
| `full` | Hard | Handle the entire triage workflow, including response generation and strategic `antigravity` balancing. |

## 📦 Getting Started

### Prerequisites
- Docker
- Python 3.10+
- OpenAI API Key (for baseline inference)

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start the environment
python main.py
```
Access the dashboard at `http://localhost:7860`.

### Docker Deployment
```bash
# Build the image
docker build -t email-env .

# Run the container
docker run -p 7860:7860 email-env
```

## 🤖 Baseline Inference
The included `inference.py` script provides a reproducible baseline score.

```bash
export OPENAI_API_KEY="your-key-here"
export MODEL_NAME="gpt-4o"
python inference.py
```

## 📂 Project Structure
- `app/`: Core logic (models, env, grader, data).
- `frontend/`: Dashboard UI (HTML, CSS, JS with Matter.js).
- `main.py`: FastAPI server entrypoint.
- `openenv.yaml`: OpenEnv metadata.
- `inference.py`: Baseline agent script.

---
Built for the **OpenEnv Round 1 Hackathon**.
