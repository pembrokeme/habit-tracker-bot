#!/usr/bin/env python3

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from database import HabitDatabase

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize database
db = HabitDatabase()

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

async def add_habit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a new habit."""
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text(
            "Please provide a habit name. Example:\n/addhabit Drink 8 glasses of water"
        )
        return

    habit_name = ' '.join(context.args)

    try:
        habit_id = db.add_habit(user_id, habit_name)
        await update.message.reply_text(
            f"✅ Great! I've added '{habit_name}' to your habits.\n"
            f"Habit ID: {habit_id}\n\n"
            f"Use /check {habit_id} to mark it as completed for today!"
        )
    except Exception as e:
        logger.error(f"Error adding habit: {e}")
        await update.message.reply_text("Sorry, there was an error adding your habit. Please try again.")

async def view_habits(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """View all user habits."""
    user_id = update.effective_user.id

    try:
        habits = db.get_user_habits(user_id)

        if not habits:
            await update.message.reply_text(
                "You don't have any habits yet! Add one with /addhabit <habit name>"
            )
            return

        message = "📋 *Your Habits:*\n\n"
        for habit in habits:
            habit_id, name, description, created_at = habit
            message += f"*{habit_id}.* {name}\n"
            if description:
                message += f"   _{description}_\n"
            message += f"   Added: {created_at[:10]}\n\n"

        message += "Use /check <id> to mark a habit as completed!"
        await update.message.reply_text(message, parse_mode='Markdown')

    except Exception as e:
        logger.error(f"Error viewing habits: {e}")
        await update.message.reply_text("Sorry, there was an error retrieving your habits.")

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token("YOUR_BOT_TOKEN_HERE").build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("addhabit", add_habit))
    application.add_handler(CommandHandler("habits", view_habits))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()