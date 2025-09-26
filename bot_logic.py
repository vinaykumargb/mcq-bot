import asyncio
import os
from datetime import datetime
from telegram import Bot
from telegram.error import TimedOut

# Load environment variables for local testing
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Safe for Render deployment (dotenv not required)

# Get Telegram bot token from environment variables
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError(
        "Telegram bot token not set! Please define TOKEN in environment variables."
    )

async def send_poll(bot, chat_id, question_text, option_question, options, correct_option_id, explanation, thread_id=None):
    """
    Sends a question as a message, then sends it as a quiz poll.
    Retries on TimedOut error.
    """
    try:
        # Send main question text
        await bot.send_message(
            chat_id=chat_id,
            text=question_text,
            message_thread_id=thread_id
        )

        # Send quiz poll
        await bot.send_poll(
            chat_id=chat_id,
            question=option_question or "Options",  # fallback if empty
            options=options,
            type="quiz",
            correct_option_id=correct_option_id,
            is_anonymous=True,
            explanation=explanation[:300],  # Telegram explanation limit
            message_thread_id=thread_id
        )
    except TimedOut:
        print("Timed out! Retrying...")
        await send_poll(bot, chat_id, question_text, option_question, options, correct_option_id, explanation, thread_id)

async def send_mcqs(data):
    """
    Send multiple MCQs to a specified chat.
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
        # Format main question text
        question_text = f"{idx}. {mcq.get('question', '')}"
        if idx == 1:
            question_text = f"#{subject}\n\n{question_text}"

        await send_poll(
            bot,
            CHAT_ID,
            question_text=question_text,
            option_question=mcq.get("option_question", "Options"),
            options=mcq.get("options", []),
            correct_option_id=mcq.get("answer", 0),
            explanation=mcq.get("explanation", ""),
            thread_id=THREAD_ID
        )

    await bot.close()
    print("All MCQs sent successfully!")

# Optional: standalone run
if __name__ == "__main__":
    import json

    # Example data
    sample_data = {
        "chat": "test",
        "subject": "Polity",
        "mcqs": [
            {
                "question": "What is the capital of India?",
                "option_question": "Options",
                "options": ["Delhi", "Mumbai", "Kolkata", "Chennai"],
                "answer": 0,
                "explanation": "Delhi is the capital of India."
            }
        ]
    }
    asyncio.run(send_mcqs(sample_data))