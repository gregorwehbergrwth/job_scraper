import asyncio
from telegram import Bot
from telegram.error import BadRequest

api_key = '7542268069:AAF7-SuiukANQ9gAhMiRQ51CIGnDRlcCANc'
user_ids = ['5623557325']


def message(txt):
    async def send_message(text):
        bot = Bot(token=api_key)
        try:
            for user_id in user_ids:
                await bot.send_message(chat_id=user_id, text=text)
        except BadRequest as e2:
            print(f"Telegram API Error: {e2}")
    try:
        # raise Exception("Blocked Message")
        asyncio.run(send_message(txt)) if txt else None
    except Exception as e:
        print(f"Error sending message: {e}")
    print(txt, end="\n")


def configure_text(new, mouse, mode, index):
    if mode == "hawk":
        return new
    else:
        job_dict = new

    structure = {
        "uniklinik": ['Titel', 'Bereich', 'Frist', 'Link'],
        "rwth": ['Titel', 'Frist', 'Veröffentlichungsdatum', 'Arbeitgeber', 'Link'],
        "un": ['Job Title', 'Duty Station', 'Job Network', 'Department/Office', 'Deadline', 'Link'],
        "trier": ['Titel', 'Arbeitgeber', 'Art', 'Link'],
        "asta_aachen": ['Titel', 'Arbeitgeber', 'Ort', 'Datum', 'Link']
    }

    try:
        text = "\n".join([job_dict.get(key, 'N/A') for key in structure[mouse]])
        return text if index != 9 else text + "\nMore than 10 new jobs found.\nCheck the website!\n"
    except Exception as e:
        return f"Error structuring message: {e}"
