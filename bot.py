#!/usr/bin/env python3

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}!\n\n"
        f"Welcome to Habit Tracker Bot! 🎯\n\n"
        f"I'll help you track your daily habits and build better routines.\n\n"
        f"Available commands:\n"
        f"/start - Show this message\n"
        f"/help - Get help\n"
        f"/addhabit - Add a new habit\n"
        f"/habits - View your habits\n"
        f"/check - Mark habit as completed"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
🎯 *Habit Tracker Bot Help*

This bot helps you track your daily habits and build better routines.

*Commands:*
/start - Start the bot and see welcome message
/help - Show this help message
/addhabit <habit name> - Add a new habit to track
/habits - View all your current habits
/check <habit id> - Mark a habit as completed for today
/stats - View your habit statistics

*Examples:*
/addhabit Drink 8 glasses of water
/addhabit Exercise for 30 minutes
/check 1

Start building better habits today! 💪
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token("YOUR_BOT_TOKEN_HERE").build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()