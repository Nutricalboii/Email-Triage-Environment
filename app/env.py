import random
from typing import Tuple, Dict, Any
from app.data import EMAILS
from app.models import Observation, Action, Reward
from app.grader import grade_action

class EmailEnv:
    def __init__(self):
        self.current_email = None
        self.gravity = 0.0
        self.done = False
        self.steps = 0
        self.max_steps = 5  # Episode ends after 5 emails or explicitly handled
        self.current_task = "full"

    def reset(self, task: str = "full") -> Observation:
        """
        Resets the environment to an initial state.
        """
        self.current_task = task
        self.current_email = random.choice(EMAILS)
        self.done = False
        self.steps = 0
        
        # Calculate gravity (urgency pull)
        # Urgent emails have higher gravity (0.6 - 1.0)
        # Normal/Spam emails have lower gravity (0.0 - 0.5)
        if self.current_email["category"] == "urgent":
            self.gravity = round(random.uniform(0.6, 1.0), 2)
        else:
            self.gravity = round(random.uniform(0.0, 0.5), 2)

        return Observation(
            email_text=self.current_email["text"],
            sender="user@example.com",
            gravity=self.gravity,
            history=[]
        )

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        """
        Processes an action, calculates rewards, and returns next state.
        """
        if self.done:
            raise Exception("Episode already finished. Call reset().")
        
        score = grade_action(action, self.current_email, self.gravity, self.current_task)
        
        # Reward shaping (partial progress)
        reward_value = score
        if score == 1.0:
            reward_value += 0.5  # Bonus for perfect triage
        elif score < 0.3:
            reward_value -= 0.2  # Penalty for clear failure
            
        reward = Reward(score=reward_value, contribution=f"Task score: {score}")

        self.steps += 1
        if self.steps >= self.max_steps:
            self.done = True
        else:
            # Move to next email in the episode
            self.current_email = random.choice(EMAILS)
            if self.current_email["category"] == "urgent":
                self.gravity = round(random.uniform(0.6, 1.0), 2)
            else:
                self.gravity = round(random.uniform(0.0, 0.5), 2)
        
        obs = Observation(
            email_text=self.current_email["text"],
            sender="user@example.com",
            gravity=self.gravity,
            history=[action.response]
        )

        return obs, reward, self.done, {"score": score}

    def state(self) -> Dict[str, Any]:
        """
        Returns the current internal state.
        """
        return {
            "email_id": self.current_email["id"],
            "category": self.current_email["category"],
            "priority": self.current_email["priority"],
            "gravity": self.gravity,
            "steps": self.steps,
            "done": self.done
        }
