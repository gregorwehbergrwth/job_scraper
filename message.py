import asyncio
from telegram import Bot
from telegram.error import BadRequest

# Environment variables for API keys and User ID (set in GitHub Secrets)
api_key = '7542268069:AAF7-SuiukANQ9gAhMiRQ51CIGnDRlcCANc'
user_id = '5623557325'

def message(text):
    async def send_message(text):
        """Send a message via Telegram."""
        bot = Bot(token=api_key)
        try:
            await bot.send_message(chat_id=user_id, text=text)
        except BadRequest as e:
            print(f"Telegram API Error: {e}")

    asyncio.run(send_message(text))