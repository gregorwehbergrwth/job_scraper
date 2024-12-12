import asyncio
from telegram import Bot
from telegram.error import BadRequest

# Environment variables for API keys and User ID (set in GitHub Secrets)
api_key = '7542268069:AAF7-SuiukANQ9gAhMiRQ51CIGnDRlcCANc'
user_ids = ['5623557325']

def message(text):
    async def send_message(text):
        """Send a message via Telegram."""
        bot = Bot(token=api_key)
        try:
            for user_id in user_ids:
                await bot.send_message(chat_id=user_id, text=text)
        except BadRequest as e:
            print(f"Telegram API Error: {e}")

    asyncio.run(send_message(text))

def configure_rwth_message(dict):
    txt = [
        f"{dict['title']}\n"
        f"Link: {dict['link']}\n"
        f"Deadline: {dict['deadline']}\n"
        f"{dict['pub_date']}\n"
        f"Arbeitgeber: {dict['location']}\n"
        f"Nummer: {dict['listing_number']}\n\n"
    ]
    txt = "\n".join(txt)
    return txt

def configure_un_message(dict):
    # txt = [
    #     f"{dict['Job Title']}\n"
    #     f"Job Network: {dict['Job Network']}\n"
    #     f"Job Family: {dict['Job Family']}\n"
    #     f"Department/Office: {dict['Department/Office']}\n"
    #     f"Duty Station: {dict['Duty Station']}\n"
    #     # f"Category and Level: {dict['Category and Level']}\n"
    #     f"Date Posted: {dict['Date Posted']}\n"
    #     f"Deadline: {dict['Deadline']}\n"
    #     # f"Job ID: {dict['Job ID']}\n"
    #     f"Link: {dict['Link']}"
    # ]
    try:
        txt = [
            f" - {dict['Job Title']}\n"
            f" - {dict['Duty Station']}\n"
            f" - Network: {dict['Job Network']}\n"
            f" - {dict['Department/Office']}\n"
            f" - Deadline: {dict['Deadline']}\n"
            f" - Link: {dict['Link']}\n"
        ]
        txt = "\n".join(txt)
    except Exception as e:
        txt = f"Error parsing listing: {e}"
    return txt
