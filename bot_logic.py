import asyncio
import json
import os
from datetime import datetime
from telegram import Bot
from telegram.error import TimedOut
from dotenv import load_dotenv  # for local testing

# Load environment variables from .env (optional, for local testing)
load_dotenv()

# Telegram bot token from environment variable
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("Telegram bot token not set! Please define TOKEN in environment variables.")

async def send_poll(bot, chat_id, question_text, option_question, options, correct_option_id, explanation, thread_id=None):
    """Send a question as text and then quiz poll."""
    try:
        # Send main question first
        await bot.send_message(
            chat_id=chat_id,
            text=question_text,
            message_thread_id=thread_id if thread_id else None
        )
        # Send quiz poll
        await bot.send_poll(
            chat_id=chat_id,
            question=option_question,
            options=options,
            type="quiz",
            correct_option_id=correct_option_id,
            is_anonymous=True,
            explanation=explanation[:300],  # Telegram limit
            message_thread_id=thread_id if thread_id else None
        )
    except TimedOut:
        print("Timed out! Retrying...")
        await send_poll(bot, chat_id, question_text, option_question, options, correct_option_id, explanation, thread_id)

async def send_mcqs(data):
    """
    data = {
        "chat": "test" or "pro",
        "subject": "Polity",
        "mcqs": [ {...}, {...} ]
    }
    """
    chat_input = data.get("chat", "test").lower()
    if chat_input == "pro":
        CHAT_ID = -1003018799293
        THREAD_ID = 3
    else:
        CHAT_ID = -1001991761209
        THREAD_ID = None

    bot = Bot(token=TOKEN)
    mcqs = data.get("mcqs", [])
    subject = data.get("subject", "General")

    today = datetime.now().strftime("%Y-%m-%d")
    for idx, mcq in enumerate(mcqs, start=1):
        if idx == 1:
            question_text = f"#{subject}\n\n{idx}. {mcq['question']}"
        else:
            question_text = f"{idx}. {mcq['question']}"

        await send_poll(
            bot,
            CHAT_ID,
            question_text=question_text,
            option_question=mcq["option_question"],
            options=mcq["options"],
            correct_option_id=mcq["answer"],
            explanation=mcq["explanation"],
            thread_id=THREAD_ID
        )

    await bot.close()
    print("All MCQs sent successfully!")