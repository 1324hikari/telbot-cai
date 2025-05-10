import asyncio
import json
import os
import time
from datetime import datetime
from PyCharacterAI import get_client
from PyCharacterAI.exceptions import SessionClosedError
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from termcolor import colored

# Import tokens from config.py
try:
    from config import (
        TELEGRAM_BOT_TOKEN,
        CHARACTER_AI_TOKEN,
        CHARACTER_ID,
        ALLOWED_USER_ID,
    )
except ImportError:
    print("Error: config.py file not found or improperly configured")
    exit(1)

CHAT_SESSION_FILE = "chat_session.json"
BOT_LOG_FILE = "bot_logs.txt"
USER_LOG_FILE = "user_messages.txt"

client = None  # CAI client
chat = None  # Current session
current_time = datetime.now()

# --------------------------
# Logging and Chat Sessions
# --------------------------

def log_to_file(log_file: str, message: str) -> None:
    """Log messages to a specified file with timestamp."""
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"{datetime.now()} - {message}\n")

def save_chat_session(chat_id: str) -> None:
    """Save the current chat session ID to a file."""
    with open(CHAT_SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump({"chat_id": chat_id}, f)

def load_chat_session() -> str | None:
    """Load the chat session ID from file if it exists."""
    if os.path.exists(CHAT_SESSION_FILE):
        with open(CHAT_SESSION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("chat_id")
    return None

# --------------------------
# Command Handlers for Telegram
# --------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command to initialize the bot and Character.AI session."""
    global client, chat

    user = update.effective_user
    if user.id != ALLOWED_USER_ID:
        print(colored(f"Unauthorized access attempt by @{user.username} (ID: {user.id})", "red"))
        log_to_file(BOT_LOG_FILE, f"Unauthorized access attempt by @{user.username} (ID: {user.id})")
        await update.message.reply_text("You are not authorized to use this bot.")
        return

    log_to_file(USER_LOG_FILE, f"User @{user.username} (ID: {user.id}) issued /start command.")

    try:
        while True:  # Reconnect to network ifn poor network connection
            try:
                if not client:
                    client = await get_client(token=CHARACTER_AI_TOKEN)
                    me = await client.account.fetch_me()
                    await update.message.reply_text(f"Connected to CharacterAI as @{me.username}.")
                    log_to_file(BOT_LOG_FILE, "Connected to CharacterAI.")

                saved_chat_id = load_chat_session()
                if saved_chat_id:
                    await update.message.reply_text("Continuing the previous conversation. Send your message!")
                else:
                    chat, greeting_message = await client.chat.create_chat(CHARACTER_ID)
                    save_chat_session(chat.chat_id)
                    greeting = greeting_message.get_primary_candidate().text
                    await update.message.reply_text(f"{greeting}")
                break
            except Exception as e:
                print(colored(f"Waiting for network... Error: {str(e)}", "yellow"))
                log_to_file(BOT_LOG_FILE, f"Waiting for network... Error: {str(e)}")
                time.sleep(5)  # Retry every 5 seconds
    except Exception as e:
        error_message = f"Error in start command: {str(e)}"
        print(colored(error_message, "red"))
        log_to_file(BOT_LOG_FILE, error_message)

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /stop command to terminate the Character.AI session."""
    global client, chat

    user = update.effective_user
    if user.id != ALLOWED_USER_ID:
        print(colored(f"Unauthorized access attempt by @{user.username} (ID: {user.id})", "red"))
        log_to_file(BOT_LOG_FILE, f"Unauthorized stop attempt by @{user.username} (ID: {user.id})")
        await update.message.reply_text("You are not authorized to use this bot.")
        return

    log_to_file(USER_LOG_FILE, f"User @{user.username} (ID: {user.id}) issued /stop command.")

    try:
        if client:
            await client.close_session()
            await update.message.reply_text("Chat session closed. Goodbye!")
            client = None
            chat = None
            if os.path.exists(CHAT_SESSION_FILE):
                os.remove(CHAT_SESSION_FILE)
            log_to_file(BOT_LOG_FILE, "Chat session closed.")
        else:
            await update.message.reply_text("No active session to close.")
    except Exception as e:
        error_message = f"Error in stop command: {str(e)}"
        print(colored(error_message, "red"))
        log_to_file(BOT_LOG_FILE, error_message)

# --------------------------
# Message Handler
# --------------------------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming text messages from authorized users."""
    global client, chat

    user = update.effective_user
    user_message = update.message.text
    log_to_file(USER_LOG_FILE, f"Message from @{user.username} (ID: {user.id}): {user_message}")

    if user.id != ALLOWED_USER_ID:
        print(colored(f"Unauthorized access attempt by @{user.username} (ID: {user.id})", "red"))
        log_to_file(BOT_LOG_FILE, f"Unauthorized message from @{user.username} (ID: {user.id}): {user_message}")
        await update.message.reply_text(
            "You are not authorized to use this bot. For more info, please message the developer @Hikarii7713"
        )
        return

    try:
        if not client:
            client = await get_client(token=CHARACTER_AI_TOKEN)

        saved_chat_id = load_chat_session()
        if not saved_chat_id:
            chat, _ = await client.chat.create_chat(CHARACTER_ID)
            save_chat_session(chat.chat_id)

        # Resend if failed to send message
        while True:
            try:
                await context.bot.send_chat_action(
                    chat_id=update.effective_chat.id, action="typing"
                )
                answer = await client.chat.send_message(
                    CHARACTER_ID, saved_chat_id, user_message
                )
                response_text = answer.get_primary_candidate().text
                save_chat_session(saved_chat_id)

                await update.message.reply_text(f"{response_text}")
                print(f"{datetime.now()} - Response: {response_text}")
                log_to_file(BOT_LOG_FILE, f"Bot Response: {response_text}")
                break
            except Exception as e:
                print(colored(f"Retrying... Waiting for network. Error: {str(e)}", "yellow"))
                log_to_file(BOT_LOG_FILE, f"Retrying... Waiting for network. Error: {str(e)}")
                time.sleep(5)
    except Exception as e:
        error_message = f"Error in message handling: {str(e)}"
        print(colored(error_message, "red"))
        log_to_file(BOT_LOG_FILE, error_message)

# --------------------------
# Main Function
# --------------------------

def main() -> None:
    """Initialize and run the Telegram bot."""
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("TelBot Version 13 - 012825")
    print("Bot is running... Press Ctrl+C to stop.")
    print("---------------------------------------")
    log_to_file(BOT_LOG_FILE, "Bot started and running.")

    try:
        app.run_polling()
    except Exception as e:
        log_to_file(BOT_LOG_FILE, f"Bot crashed: {str(e)}")
        print(colored(f"Bot crashed: {str(e)}", "red"))

if __name__ == "__main__":
    asyncio.run(main())
