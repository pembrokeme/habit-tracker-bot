#!/bin/bash

# Habit Tracker Bot Runner Script
# This script sets up the environment and runs the bot

set -e

echo "🚀 Starting Habit Tracker Bot..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if config.py exists
if [ ! -f "config.py" ]; then
    echo "❌ config.py not found!"
    echo "Please copy config_example.py to config.py and add your bot token."
    exit 1
fi

# Run the bot
echo "🤖 Starting the bot..."
python bot.py