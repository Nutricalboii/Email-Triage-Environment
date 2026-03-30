import os
import requests
import json
from app.data import EMAILS
from app.models import Action

# Configuration
BASE_URL = "http://localhost:7860"

class OpenEnvValidator:
    def __init__(self):
        self.results = []
        self.errors = 0
        self.warnings = 0

    def log(self, type, message, success=True):
        status = "✅ PASS" if success else ("❌ FAIL" if type == "ERROR" else "⚠️ WARN")
        if type == "ERROR": self.errors += 1
        if type == "WARN": self.warnings += 1
        print(f"{status} | {message}")
        self.results.append({"type": type, "message": message, "success": success})

    def run_checks(self):
        print("=== OpenEnv Environment Validator (30-Point Check) ===\n")
        
        # 1. Infrastructure Checks
        self.check_files()
        
        # 2. Data Integrity
        self.check_dataset()
        
        # 3. API & Spec Compliance (Requires server running)
        self.check_api()
        
        # 4. Grading Logic
        self.check_grading()

        # Summary
        print(f"\n--- Validation Complete ---")
        print(f"Errors: {self.errors} | Warnings: {self.warnings}")
        if self.errors == 0:
            print("🚀 STATUS: Environment is Ready for Submission!")
        else:
            print("🛑 STATUS: Issues found. Please fix before submitting.")

    def check_files(self):
        print("[1/4] Infrastructure Checks...")
        required_files = [
            "openenv.yaml", "Dockerfile", "main.py", "app/env.py", 
            "app/grader.py", "app/data.py", "app/models.py", "README.md",
            "frontend/index.html", "frontend/style.css", "frontend/script.js"
        ]
        for f in required_files:
            exists = os.path.exists(f)
            self.log("ERROR" if not exists else "INFO", f"File '{f}' exists", exists)

    def check_dataset(self):
        print("\n[2/4] Dataset Integrity...")
        self.log("INFO", f"Dataset contains {len(EMAILS)} emails", len(EMAILS) >= 50)
        
        keys = ["id", "text", "category", "priority", "keywords", "difficulty"]
        all_keys = True
        for e in EMAILS:
            for k in keys:
                if k not in e:
                    all_keys = False
                    self.log("ERROR", f"Email ID {e.get('id')} missing key: {k}", False)
        if all_keys:
            self.log("INFO", "All emails have required schema fields", True)

        # Check adversarial coverage
        adversarial = [e for e in EMAILS if e.get("adversarial")]
        self.log("INFO", f"Adversarial coverage: {len(adversarial)} cases", len(adversarial) >= 3)

    def check_api(self):
        print("\n[3/4] API & Spec Compliance...")
        try:
            # Check Reset
            r = requests.get(f"{BASE_URL}/reset")
            self.log("ERROR" if r.status_code != 200 else "INFO", "API /reset reachable", r.status_code == 200)
            
            # Check State
            r = requests.get(f"{BASE_URL}/state")
            self.log("ERROR" if r.status_code != 200 else "INFO", "API /state reachable", r.status_code == 200)
            
            # Check Step
            test_action = {
                "category": "normal",
                "priority": "medium",
                "response": "Validation test response.",
                "antigravity": 0.5
            }
            r = requests.post(f"{BASE_URL}/step", json=test_action)
            self.log("ERROR" if r.status_code != 200 else "INFO", "API /step operational", r.status_code == 200)
            
        except Exception as e:
            self.log("WARN", f"API server not running at {BASE_URL}. Skipping live checks.", False)

    def check_grading(self):
        print("\n[4/4] Grading Logic Stress Test...")
        from app.grader import grade_action
        
        # Test trap 1: Fake Urgency
        trap_email = next(e for e in EMAILS if e['id'] == 21)
        action = Action(category="normal", priority="high", response="urgent action!", antigravity=0.5)
        score = grade_action(action, trap_email, 0.5)
        self.log("INFO", f"Trap 1 (Fake Urgency) penalty working (Score: {score})", score < 0.7)

        # Test trap 2: Polite Crisis
        trap_email = next(e for e in EMAILS if e['id'] == 22)
        action = Action(category="urgent", priority="low", response="ignore for now.", antigravity=0.5)
        score = grade_action(action, trap_email, 0.5)
        self.log("INFO", f"Trap 2 (Polite Crisis) penalty working (Score: {score})", score < 0.7)

if __name__ == "__main__":
    validator = OpenEnvValidator()
    validator.run_checks()
