import random
random.seed(42)

EMAILS = [
    {
        "id": 1,
        "text": "Your account has been hacked! Click here to reset your password immediately.",
        "category": "urgent",
        "priority": "high",
        "keywords": ["urgent", "security", "hacked", "reset", "password"],
        "difficulty": 1
    },
    {
        "id": 2,
        "text": "Get 50% off all sneakers this weekend only. Don't miss out on this deal!",
        "category": "spam",
        "priority": "low",
        "keywords": ["deal", "offer", "discount", "sneakers"],
        "difficulty": 1
    },
    {
        "id": 3,
        "text": "Can we confirm our meeting for tomorrow at 10 AM? Let me know if that works.",
        "category": "normal",
        "priority": "medium",
        "keywords": ["meeting", "confirm", "schedule", "tomorrow"],
        "difficulty": 2
    },
    {
        "id": 4,
        "text": "Critical server failure in the production cluster. Immediate action required.",
        "category": "urgent",
        "priority": "high",
        "keywords": ["failure", "critical", "server", "production", "immediate"],
        "difficulty": 1
    },
    {
        "id": 5,
        "text": "You've won a $1000 gift card! Claim your prize now by clicking this link.",
        "category": "spam",
        "priority": "low",
        "keywords": ["won", "prize", "gift card", "claim"],
        "difficulty": 1
    },
    {
        "id": 6,
        "text": "I've reviewed the design documents. Please find my comments attached.",
        "category": "normal",
        "priority": "medium",
        "keywords": ["design", "comments", "review", "attached"],
        "difficulty": 2
    },
    {
        "id": 7,
        "text": "Request for urgent approval on the Q3 budget. Deadline is end of day.",
        "category": "urgent",
        "priority": "high",
        "keywords": ["approval", "budget", "deadline", "urgent"],
        "difficulty": 3
    },
    {
        "id": 8,
        "text": "Subscribe to our newsletter and get the latest updates on AI technology.",
        "category": "spam",
        "priority": "low",
        "keywords": ["subscribe", "newsletter", "updates", "latest"],
        "difficulty": 2
    },
    {
        "id": 9,
        "text": "Looking forward to our coffee chat on Friday. See you there!",
        "category": "normal",
        "priority": "low",
        "keywords": ["coffee", "chat", "friday", "see you"],
        "difficulty": 2
    },
    {
        "id": 10,
        "text": "Security Alert: New login from an unrecognized device in Paris, France.",
        "category": "urgent",
        "priority": "high",
        "keywords": ["security", "alert", "login", "unrecognized"],
        "difficulty": 1
    },
    {
        "id": 11,
        "text": "Congratulations! You've been selected for a free cruise to the Bahamas.",
        "category": "spam",
        "priority": "low",
        "keywords": ["congratulations", "selected", "free", "cruise"],
        "difficulty": 1
    },
    {
        "id": 12,
        "text": "Can you please send me the latest version of the proposal?",
        "category": "normal",
        "priority": "medium",
        "keywords": ["proposal", "version", "send", "latest"],
        "difficulty": 2
    },
    {
        "id": 13,
        "text": "Warning: Your subscription will expire in 24 hours. Renew now to avoid interruption.",
        "category": "urgent",
        "priority": "high",
        "keywords": ["warning", "expire", "renew", "subscription"],
        "difficulty": 2
    },
    {
        "id": 14,
        "text": "Special offer: Get 3 months of premium service for the price of 1.",
        "category": "spam",
        "priority": "low",
        "keywords": ["special", "offer", "premium", "price"],
        "difficulty": 2
    },
    {
        "id": 15,
        "text": "I'll be out of the office starting tomorrow. Please contact John for urgent matters.",
        "category": "normal",
        "priority": "low",
        "keywords": ["out of the office", "contact", "urgent", "tomorrow"],
        "difficulty": 3
    },
    {
        "id": 16,
        "text": "Urgent: Payment for invoice #4592 is past due. Please settle immediately.",
        "category": "urgent",
        "priority": "high",
        "keywords": ["invoice", "payment", "past due", "settle", "urgent"],
        "difficulty": 2
    },
    {
        "id": 17,
        "text": "Discover how to double your income in just 30 days! Watch our free webinar.",
        "category": "spam",
        "priority": "low",
        "keywords": ["income", "webinar", "double", "free"],
        "difficulty": 2
    },
    {
        "id": 18,
        "text": "The team meeting has been moved to Room 4B. See you all at 2 PM.",
        "category": "normal",
        "priority": "low",
        "keywords": ["meeting", "room", "moved", "team"],
        "difficulty": 1
    },
    {
        "id": 19,
        "text": "Security update required for your workstations. Please follow the link to install.",
        "category": "urgent",
        "priority": "medium",
        "keywords": ["security", "update", "update", "install"],
        "difficulty": 2
    },
    {
        "id": 20,
        "text": "You've matched with someone new on the dating app. Check your profile!",
        "category": "spam",
        "priority": "low",
        "keywords": ["matched", "dating", "profile", "app"],
        "difficulty": 2
    },
    {
        "id": 21,
        "text": "URGENT: Pizza Party Confirmation Needed ASAP!!! We need your dietary requirements by 4 PM today or you won't get any food. PLEASE RESPOND IMMEDIATELY!!",
        "category": "normal",
        "priority": "medium",
        "keywords": ["pizza", "dietary", "confirm", "immediately"],
        "difficulty": 3,
        "adversarial": True,
        "reason": "Fake Urgency Trap: Uses extreme urgency keywords ('ASAP', 'IMMEDIATELY') for a low-priority social event."
    },
    {
        "id": 22,
        "text": "Quick check-in: I'm noticing a few repeated timeout errors in the production logs for the main payment gateway. No rush, but might be worth a look when you have a moment.",
        "category": "urgent",
        "priority": "high",
        "keywords": ["timeout", "production", "logs", "gateway"],
        "difficulty": 3,
        "adversarial": True,
        "reason": "Polite Crisis Trap: Describes a critical failure (payment gateway timeout) in a calm, professional tone without urgent keywords."
    },
    {
        "id": 23,
        "text": "Security Alert: A new device has logged into your Netflix account from Moscow, Russia. If this wasn't you, click here to secure your account within 24 hours.",
        "category": "spam",
        "priority": "low",
        "keywords": ["security", "alert", "login", "secure"],
        "difficulty": 3,
        "adversarial": True,
        "reason": "Legitimate-looking phish - mimics common security alerts to trick agents into over-prioritizing spam."
    },
    {
        "id": 24,
        "text": "The Q4 roadmap is ready for review. Please provide your feedback by Friday.",
        "category": "normal",
        "priority": "medium",
        "keywords": ["roadmap", "review", "feedback", "q4"],
        "difficulty": 2
    },
    {
        "id": 25,
        "text": "Congratulations, you've been selected as a finalist for our annual raffle! Click to claim your prize.",
        "category": "spam",
        "priority": "low",
        "keywords": ["finalist", "raffle", "prize", "claim"],
        "difficulty": 1
    },
    {
        "id": 26,
        "text": "Urgent attention required: Production database connection pooling has exceeded the limit. Possible service interruption within the next hour.",
        "category": "urgent",
        "priority": "high",
        "keywords": ["urgent", "production", "database", "limit", "interruption"],
        "difficulty": 2
    },
    {
        "id": 27,
        "text": "Can we schedule a one-on-one for this afternoon to discuss the recent project updates?",
        "category": "normal",
        "priority": "medium",
        "keywords": ["one-on-one", "discuss", "updates", "project"],
        "difficulty": 2
    },
    {
        "id": 28,
        "text": "Exclusive offer: Get a lifetime subscription to our VPN service for just $99. Limited time only!",
        "category": "spam",
        "priority": "low",
        "keywords": ["exclusive", "offer", "lifetime", "vpn", "$99"],
        "difficulty": 2
    },
    {
        "id": 29,
        "text": "Incident Report: Deployment of v2.4.1 failed on the staging environment. Rolling back now.",
        "category": "urgent",
        "priority": "high",
        "keywords": ["incident", "deployment", "failed", "staging", "rollback"],
        "difficulty": 3
    },
    {
        "id": 30,
        "text": "Please find the signed contract for the new vendor proposal attached.",
        "category": "normal",
        "priority": "medium",
        "keywords": ["signed", "contract", "vendor", "proposal", "attached"],
        "difficulty": 2
    },
    {
        "id": 31,
        "text": "Final notice: Your domain registration will expire in 48 hours. Renew today to avoid losing your URL.",
        "category": "urgent",
        "priority": "high",
        "keywords": ["final notice", "expire", "renew", "domain", "registration"],
        "difficulty": 2
    },
    {
        "id": 32,
        "text": "You're invited to a free webinar on the future of generative AI in marketing.",
        "category": "spam",
        "priority": "low",
        "keywords": ["invited", "free", "webinar", "generative ai", "marketing"],
        "difficulty": 2
    },
    {
        "id": 33,
        "text": "The office will be closed on Monday for the public holiday. Have a great weekend!",
        "category": "normal",
        "priority": "low",
        "keywords": ["closed", "monday", "holiday", "weekend"],
        "difficulty": 1
    },
    {
        "id": 34,
        "text": "Immediate action: Unauthorized access detected from unknown IP. Login blocked temporarily.",
        "category": "urgent",
        "priority": "high",
        "keywords": ["immediate", "unauthorized", "access", "unknown", "blocked"],
        "difficulty": 1
    },
    {
        "id": 35,
        "text": "Take our survey and win a $25 Amazon gift card. Your feedback is important!",
        "category": "spam",
        "priority": "low",
        "keywords": ["survey", "win", "gift card", "amazon", "feedback"],
        "difficulty": 2
    },
    {
        "id": 36,
        "text": "Can you check the logs for the user authentication service? We're seeing some latency.",
        "category": "normal",
        "priority": "medium",
        "keywords": ["logs", "authentication", "latency", "check"],
        "difficulty": 3
    },
    {
        "id": 37,
        "text": "CRITICAL: Security vulnerability found in dependency 'request-lib' v1.2. Please update immediately.",
        "category": "urgent",
        "priority": "high",
        "keywords": ["critical", "vulnerability", "dependency", "security", "update"],
        "difficulty": 2
    },
    {
        "id": 38,
        "text": "Hot deals: Up to 70% off electronics! Shop our summer sale now.",
        "category": "spam",
        "priority": "low",
        "keywords": ["deals", "electronics", "shop", "sale", "70%"],
        "difficulty": 1
    },
    {
        "id": 39,
        "text": "I'll be working remotely today. Reach out on Slack if you need me.",
        "category": "normal",
        "priority": "low",
        "keywords": ["remotely", "reach out", "slack", "working"],
        "difficulty": 1
    },
    {
        "id": 40,
        "text": "URGENT: Legal notice regarding the use of licensed materials in the public campaign.",
        "category": "urgent",
        "priority": "high",
        "keywords": ["urgent", "legal", "notice", "licensed", "materials"],
        "difficulty": 2
    },
    {
        "id": 41,
        "text": "Discover your dream home with our AI-powered property search tool.",
        "category": "spam",
        "priority": "low",
        "keywords": ["dream home", "ai-powered", "property", "search"],
        "difficulty": 2
    },
    {
        "id": 42,
        "text": "The minutes of the steering committee meeting are now available on the shared drive.",
        "category": "normal",
        "priority": "low",
        "keywords": ["minutes", "steering committee", "meeting", "shared drive"],
        "difficulty": 2
    },
    {
        "id": 43,
        "text": "ALERT: Abnormal outgoing traffic detected from server SRV-4029. Investigating now.",
        "category": "urgent",
        "priority": "high",
        "keywords": ["alert", "abnormal", "traffic", "detected", "investigating"],
        "difficulty": 3
    },
    {
        "id": 44,
        "text": "Become a certified cloud expert in just 4 weeks! Enroll in our intensive bootcamp.",
        "category": "spam",
        "priority": "low",
        "keywords": ["certified", "cloud", "expert", "enroll", "bootcamp"],
        "difficulty": 3
    },
    {
        "id": 45,
        "text": "Could you please review the latest draft of the press release?",
        "category": "normal",
        "priority": "medium",
        "keywords": ["review", "draft", "press release", "latest"],
        "difficulty": 2
    },
    {
        "id": 46,
        "text": "CRITICAL: Payment gateway down. Unable to process new customer orders.",
        "category": "urgent",
        "priority": "high",
        "keywords": ["critical", "payment gateway", "down", "process", "orders"],
        "difficulty": 1
    },
    {
        "id": 47,
        "text": "Unlock the secret to early retirement! Join our exclusive investment mastermind.",
        "category": "spam",
        "priority": "low",
        "keywords": ["unlock", "secret", "retirement", "investment", "mastermind"],
        "difficulty": 3
    },
    {
        "id": 48,
        "text": "The monthly lunch-and-learn session is scheduled for Thursday at noon in the café.",
        "category": "normal",
        "priority": "low",
        "keywords": ["lunch-and-learn", "session", "thursday", "noon", "café"],
        "difficulty": 1
    },
    {
        "id": 49,
        "text": "Emergency: Water leak detected in the server room. All staff please avoid the area.",
        "category": "urgent",
        "priority": "high",
        "keywords": ["emergency", "water leak", "server room", "avoid", "detected"],
        "difficulty": 1
    },
    {
        "id": 50,
        "text": "Your prescription is ready for pickup at our pharmacy. Visit us today!",
        "category": "spam",
        "priority": "low",
        "keywords": ["prescription", "ready", "pickup", "pharmacy", "visit"],
        "difficulty": 2
    },
    {
        "id": 51,
        "text": "Can you please update the team on the current status of the API integration?",
        "category": "normal",
        "priority": "medium",
        "keywords": ["update", "team", "status", "api integration", "integration"],
        "difficulty": 2
    },
    {
        "id": 52,
        "text": "URGENT: Server room temperature has exceeded the threshold! Shutdown may be necessary.",
        "category": "urgent",
        "priority": "high",
        "keywords": ["urgent", "temperature", "threshold", "shutdown", "exceeded"],
        "difficulty": 1
    },
    {
        "id": 53,
        "text": "Join our network and earn extra cash from the comfort of your home.",
        "category": "spam",
        "priority": "low",
        "keywords": ["join", "earn", "cash", "comfort", "home"],
        "difficulty": 2
    }
]
