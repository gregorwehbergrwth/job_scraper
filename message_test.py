import time
import asyncio
from telegram import Bot
from telegram.error import BadRequest, TimedOut, NetworkError

api_key = '8030882097:AAHyDEN1DWhyRYUhbUOBA8b-Gz0AIpOEJlg'
user_id = '5623557325'
_bot = None


def problem(mouse, error, send_message=True):
    print(f"Problem in {mouse}: {error}")


_bot = None


def get_bot():
    global _bot

    if _bot is None:
        _bot = Bot(token=api_key)

    return _bot


def send_message(text, bot):
    try:
        bot.send_message(chat_id=user_id, text=text)
        return True
    except (BadRequest, TimedOut, NetworkError) as e:
        problem(mouse="send_message", error=f"Error sending to {user_id}: {e}")
        return False


def messages(texte, test=False):
    _bot = get_bot()
    try:
        unsend_messages = []
        if not test:
            for message in texte:
                if send_message(message, _bot):
                    pass
                else:
                    unsend_messages.append(message)
        if unsend_messages:
            messages(texte)
    except Exception as e:
        problem(mouse="messages", error=f"Critical error: {e}")
    finally:
        print(*texte, sep="\n") if texte else print("No new messages to send.")



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
