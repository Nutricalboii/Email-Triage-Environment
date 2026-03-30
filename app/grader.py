from app.models import Action

def grade_action(action: Action, email: dict, gravity: float, task: str = "full") -> float:
    """
    Programmatically scores the agent's action.
    Returns a score between 0.0 and 1.0.
    """
    score = 0.0
    
    # Task 1: Basic classification (40% weight)
    if action.category == email["category"]:
        score += 0.4
    
    if task == "classification":
        return min(round(score / 0.4, 2), 1.0)
    
    # Task 2: Priority assignment (30% weight)
    # If priority matches, add points.
    if action.priority == email["priority"]:
        score += 0.3
    
    if task == "priority":
        return min(round(score / 0.7, 2), 1.0)
    
    # Task 3: Full triage (30% remaining)
    # - Response relevance (15%)
    response_lower = action.response.lower()
    keyword_matches = sum(1 for kw in email["keywords"] if kw.lower() in response_lower)
    if email["keywords"]:
        response_score = (keyword_matches / len(email["keywords"])) * 0.15
        score += response_score
    
    # - Antigravity strategy (15%)
    # Logic: High gravity emails should have low antigravity (action now).
    # Low gravity emails can have high antigravity (strategic delay).
    # Ideal: antigravity ~= 1.0 - gravity
    strategy_diff = abs(action.antigravity - (1.0 - gravity))
    if strategy_diff < 0.2:
        score += 0.15
    elif strategy_diff < 0.4:
        score += 0.07
        
    return round(score, 2)
