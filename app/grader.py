from app.models import Action

def grade_action(action: Action, email: dict, gravity: float, task: str = "full") -> dict:
    """
    Programmatically scores the agent's action.
    Returns a dictionary with 'score' and 'mistake' (if any).
    """
    score = 0.0
    mistake = None
    
    # Task 1: Basic classification (40% weight)
    if action.category == email["category"]:
        score += 0.4
    
    if task == "classification":
        return {"score": min(round(score / 0.4, 2), 1.0), "mistake": None}
    
    # Task 2: Priority assignment (30% weight)
    if action.priority == email["priority"]:
        score += 0.3
    
    if task == "priority":
        return {"score": min(round(score / 0.7, 2), 1.0), "mistake": None}
    
    # Task 3: Full triage (30% remaining)
    # - Response relevance (15%)
    response_lower = action.response.lower()
    keyword_matches = sum(1 for kw in email["keywords"] if kw.lower() in response_lower)
    if email["keywords"]:
        response_score = (keyword_matches / len(email["keywords"])) * 0.15
        score += response_score
    
    # - Antigravity strategy (15%)
    # Logic: High gravity emails should have low antigravity (action now).
    strategy_diff = abs(action.antigravity - (1.0 - gravity))
    if strategy_diff < 0.15: # Refined: tighter threshold for "Expert" tier
        score += 0.15
    elif strategy_diff < 0.3:
        score += 0.07

    # --- Adversarial Trap Penalties ---
    # Trap 1: Fake Urgency (Normal email with urgent words)
    if email.get("id") == 21 and action.priority == "high":
        penalty = 0.4
        score -= penalty
        mistake = "Fell for 'Fake Urgency' trap: prioritized a social event over critical tasks due to surface-level keywords."
    
    # Trap 2: Polite Crisis (Urgent email without urgent words)
    if email.get("id") == 22 and action.priority != "high":
        penalty = 0.4
        score -= penalty
        mistake = "Fell for 'Polite Crisis' trap: ignored a critical production failure because it lacked aggressive urgent keywords."
        
    # Trap 3: Legitimate Phish (Spam mimicking alerts)
    if email.get("id") == 23 and action.category != "spam":
        penalty = 0.4
        score -= penalty
        mistake = "Fell for 'Deceptive Phish' trap: misidentified sophisticated spam as a legitimate security alert."

    return {"score": round(max(0.0, score), 2), "mistake": mistake}
