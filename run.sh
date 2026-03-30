#!/bin/bash

# OpenEnv Email Triage - One-Click Launcher
echo "🚀 Initializing OpenEnv Email Triage Assistant..."

# 1. Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Error: Could not create virtual environment. You may need to run: sudo apt install python3-venv"
        exit 1
    fi
fi

# 2. Activate virtual environment
echo "🔗 Activating environment..."
source venv/bin/activate

# 3. Install/Update dependencies
echo "📥 Installing dependencies (this may take a minute)..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# 4. Launch the server
echo "⚡ Starting FastAPI server on http://localhost:7860..."
echo "--------------------------------------------------------"
python main.py
