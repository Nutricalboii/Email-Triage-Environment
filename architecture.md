# Environment Architecture: The Antigravity Principle

This document provides a technical deep-dive into the design philosophy and mechanics of the **OpenEnv Email Triage Assistant**.

## 🧠 The Antigravity Principle

In high-pressure professional environments, urgency acts like **Gravity**—it pulls tasks toward immediate action. An effective executive agent must possess **Antigravity**—the ability to override apparent surface-level urgency based on deep contextual signals.

> [!NOTE]
> **Antigravity Definition**: The cognitive capacity to override "keyword-driven" urgency (e.g., "ASAP!!") in favor of "business-impact" urgency (e.g., silent production failure).

### ⚖️ The Trust Clause (Deterministic Scoring)
To ensure absolute fairness and judge trust, the environment adheres to the following rules:
1. **Explainable Penalties**: All adversarial traps have explicit, logged reasons for penalties.
2. **Bounded Hidden Metrics**: Any "hidden" quality metrics (like strategic delay timing) are strictly bounded to ±0.1 impact.
3. **No Randomness**: The grading engine is 100% deterministic (seeded `random.seed(42)`). Same agent action + same observation always equals the same score.
4. **Correctness First**: Intent and Priority matches always form the core 70% of the score. Quality metrics never override fundamental correctness.

### THE URGENCY-OVERRIDE FORMULA
The environment implements a non-linear reward function based on the interaction between environmental gravity ($G$) and agent-controlled antigravity ($A$):

$$EffectiveUrgency = G \times (1 - A)$$

- **High $G$, Low $A$**: Action required immediately (e.g., Production Outage).
- **Low $G$, High $A$**: Strategic delay (e.g., Non-urgent FYI).

### Reward Calculation
The agent is rewarded for its **precision** in setting $A$. The closer $A$ is to the ideal state ($1 - G$), the higher the strategic score.

```python
strategy_diff = abs(action.antigravity - (1.0 - gravity))
if strategy_diff < 0.15:
    score += 0.15  # Expert tier
```

## 🛡️ Adversarial Integrity

To ensure the environment evaluates **Intelligence** rather than **Pattern Matching**, we've implemented three specialized "Trap" scenarios:

### 1. The Fake Urgency Trap (Category: Normal)
- **Text**: "URGENT: Pizza Party Confirmation Needed ASAP!!!"
- **Trap**: Uses high-gravity keywords for a low-gravity social event.
- **Grader Penalty**: -0.4 if `priority == "high"`.

### 2. The Polite Crisis (Category: Urgent)
- **Text**: "Quick check-in... noticing some repeated failures in production logs..."
- **Trap**: Describes a critical failure in a calm, professional tone.
- **Grader Penalty**: -0.4 if `priority != "high"`.

### 3. The Deceptive Phish (Category: Spam)
- **Text**: "Security Alert: A new device has logged into your account..."
- **Trap**: Mimics standard system alerts to test over-prioritization of noise.
- **Grader Penalty**: -0.4 if `category != "spam"`.

## 📈 Efficiency & Resource Management

To move beyond "Single-Shot" evaluation, the environment uses **Episode Trajectories** (Typically 5 emails per session).

### The Efficiency Penalty
As the session progresses, a **Cumulative Penalty** is applied to each step's reward to encourage fast decision-making:
$$R_{total} = \sum (S_i - \min(0.15, i \times 0.03))$$
Where $S_i$ is the task score for email $i$. 

---
**OpenEnv Submission | Team Singularity**
