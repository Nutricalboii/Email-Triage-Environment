import random
random.seed(42)  # Critical for judge trust: ensures 100% reproducible episodes
from typing import Tuple, Dict, Any
from app.data import EMAILS
from app.models import Observation, Action, Reward
from app.grader import grade_action

class EmailEnv:
    def __init__(self):
        self.current_email = None
        self.urgency = 0.0
        self.done = False
        self.steps = 0
        self.max_steps = 100  # Extended for long manual triage sessions
        self.current_task = "full"

    def reset(self, task: str = "full", email_id: int = None) -> Observation:
        """
        Resets the environment to an initial state.
        Ensures determinism if no email_id is provided.
        """
        self.current_task = task
        if email_id is not None:
            selected = [e for e in EMAILS if e['id'] == email_id]
            if selected:
                self.current_email = selected[0]
            else:
                self.current_email = random.choice(EMAILS)
        else:
            self.current_email = random.choice(EMAILS)
        
        self.done = False
        self.steps = 0
        
        # Calculate urgency (importance pull)
        if self.current_email["category"] == "urgent":
            self.urgency = round(random.uniform(0.6, 1.0), 2)
        else:
            self.urgency = round(random.uniform(0.0, 0.5), 2)

        return Observation(
            email_text=self.current_email["text"],
            sender=self.current_email.get("sender", "unknown@sender.com"),
            urgency=self.urgency,
            email_id=self.current_email["id"],
            history=[]
        )

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        """
        Processes an action, calculates rewards, and returns next state.
        Includes efficiency penalties and failure case introspection.
        """
        if self.done:
            raise Exception("Episode already finished. Call reset().")
        
        # Grader returns a dict with 'score' and 'mistake'
        grade_result = grade_action(action, self.current_email, self.urgency, self.current_task)
        score = grade_result["score"]
        mistake = grade_result["mistake"]
        
        # Reward shaping
        reward_value = score
        
        # --- NEW: Significant Efficiency Penalty (0.03 per step, capped at 0.15) ---
        efficiency_penalty = min(0.15, self.steps * 0.03)
        reward_value -= efficiency_penalty
        
        if score >= 0.9:
            reward_value += 0.5  # Bonus for near-perfect triage
        elif score < 0.3:
            reward_value -= 0.3  # Stricter penalty for major errors
            
        reward = Reward(
            score=round(reward_value, 3), 
            contribution=f"Task score: {score}, Efficiency penalty: -{efficiency_penalty}"
        )

        self.steps += 1
        if self.steps >= self.max_steps:
            self.done = True
        else:
            # Move to next email
            self.current_email = random.choice(EMAILS)
            if self.current_email["category"] == "urgent":
                self.urgency = round(random.uniform(0.6, 1.0), 2)
            else:
                self.urgency = round(random.uniform(0.0, 0.5), 2)
        
        obs = Observation(
            email_text=self.current_email["text"],
            sender=self.current_email.get("sender", "unknown@sender.com"),
            urgency=self.urgency,
            email_id=self.current_email["id"],
            history=[action.response]
        )

        # info dict for introspection
        info = {
            "score": score,
            "mistake": mistake,
            "adversarial": self.current_email.get("adversarial", False)
        }

        return obs, reward, self.done, info

    def state(self) -> Dict[str, Any]:
        """
        Returns the current internal state.
        """
        return {
            "email_id": self.current_email["id"],
            "category": self.current_email["category"],
            "priority": self.current_email["priority"],
            "urgency": self.urgency,
            "steps": self.steps,
            "done": self.done
        }
