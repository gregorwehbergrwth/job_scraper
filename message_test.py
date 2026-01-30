import time
import asyncio
import json
import asyncio
from telegram import Bot
from telegram.error import BadRequest
import re

api_key = '8030882097:AAHyDEN1DWhyRYUhbUOBA8b-Gz0AIpOEJlg'
user_ids = ['5623557325']
_bot = None


def problem(mouse, error, send_message=True):
    print(f"Problem in {mouse}: {error}")




semaphore = asyncio.Semaphore(5)
_bot = None


def get_bot():
    global _bot

    if _bot is None:
        _bot = Bot(token=api_key)

    return _bot


def messages(texte, test=False):

    async def send_one(user_id, text):
        async with semaphore:
            await _bot.send_message(chat_id=user_id, text=text)

    async def send_message_async(texts):
        _bot = get_bot()
        tasks = [send_one(user_id, text) for text in texts for user_id in user_ids]
        try:
            await asyncio.gather(*tasks)
        except BadRequest as e:
            print(f"Telegram API Error: {e}")

    try:
        if not test and texte:
            asyncio.run(send_message_async(texte))
    except Exception as e:
        problem(mouse="message", error=f"Error sending message: {e}", send_message=False)
    finally:
        print(*texte, sep="\n")



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
