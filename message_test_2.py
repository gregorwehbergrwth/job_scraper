from telegram import Bot
import time
from telegram.error import BadRequest, TimedOut, NetworkError
import asyncio

api_key = '8030882097:AAHyDEN1DWhyRYUhbUOBA8b-Gz0AIpOEJlg'
user_id = '5623557325'

_bot = None


def problem(mouse, error):
    print(f"Problem in {mouse}: {error}")


def get_bot():
    global _bot
    if _bot is None:
        _bot = Bot(token=api_key)
    return _bot

def message(txt, test=False):
    async def send_message(text):
        bot = get_bot()
        try:
            await bot.send_message(chat_id=user_id, text=text)
        except BadRequest as e2:
            print(f"Telegram API Error: {e2}")

    try:
        if not test:
            asyncio.run(send_message(txt)) if txt else None
    except Exception as e:
        problem(mouse="message", error=f"Error sending message: {e}")
    finally:
        print(txt, end="\n")

def messages(texte):
    for text in texte:
        message(text)

test_messages = [
    "Test message 1",
    "Test message 2",
    "Test message 2öaskdgöasdbgböaskdbgaösjbgaöskgjb",
    "Test message 2öaskdgöasdbgböaskdbgaösjbgaöskgjb",
    "Test message 2öaskdgöasdbgböaskdbgaösjbgaöskgjb",
    "Test message 2öaskdgöasdbgböaskdbgaösjbgaöskgjb",
    "Test message 2öaskdgöasdbgböaskdbgaösjbgaöskgjb",
    "Test message 2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb",
    "Test message 2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb",
    "Test message 2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb",
    "Test message 2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb",
    "Test message 2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb",
    "Test message 2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb2öaskdgöasdbgböaskdbgaösjbgaöskgjb",
    "Test message 2öaskdgöasdbgböaskdbgaösjbgaöskgjb",
    "Test message 2",
    "Test message 2",
    "Test message 2",
    "Test message 2",
    "Test message 2",
    "Test message 2",
    "Test message 2",
    "Test message 2",
    "Test message 2",
    "Test message 2",
    "Test message 3"
]

if __name__ == "__main__":
    start_new = time.perf_counter()
    messages(test_messages)
    print("New message time:", time.perf_counter() - start_new)
