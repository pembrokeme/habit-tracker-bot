# Habit Tracker Bot

A simple and effective Telegram bot to help you track daily habits and build better routines.

## Features

- ✨ Add new habits to track with simple commands
- ✅ Check off completed habits daily
- 📊 View detailed habit statistics and progress
- 🔥 Track streaks and completion rates
- 💾 Persistent SQLite database storage
- 🤖 Easy-to-use Telegram interface

## Commands

- `/start` - Welcome message and overview
- `/help` - Get help with commands
- `/addhabit <habit name>` - Add a new habit
- `/habits` - View all your habits
- `/check <habit id>` - Mark habit as completed for today
- `/stats` - View your habit statistics

## Quick Start

1. Clone this repository
2. Copy `config_example.py` to `config.py`
3. Add your Telegram bot token to `config.py`
4. Run `./run.sh` to start the bot

## Requirements

- Python 3.8+
- python-telegram-bot library
- SQLite (included with Python)

## Installation

```bash
# Clone the repository
git clone https://github.com/pembrokeme/habit-tracker-bot.git
cd habit-tracker-bot

# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp config_example.py config.py
# Edit config.py and add your bot token

# Run the bot
python bot.py
```

## Examples

```
/addhabit Drink 8 glasses of water
/addhabit Exercise for 30 minutes
/addhabit Read for 15 minutes

/habits
/check 1
/stats
```

## License

MIT License - feel free to use and modify as needed!