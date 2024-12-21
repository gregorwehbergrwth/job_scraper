import asyncio
from telegram import Bot
from telegram.error import BadRequest

api_key = '7542268069:AAF7-SuiukANQ9gAhMiRQ51CIGnDRlcCANc'
user_ids = ['5623557325']


def message(txt):
    async def send_message(text):
        """Send a message via Telegram."""
        bot = Bot(token=api_key)
        try:
            for user_id in user_ids:
                await bot.send_message(chat_id=user_id, text=text)
        except BadRequest as e:
            print(f"Telegram API Error: {e}")
    try:
        asyncio.run(send_message(txt))
    except Exception as e:
        print(f"Error sending message: {e}")
    print(txt, end="\n")


def configure_message(job_dict, mouse):
    structure = {
        "rwth": [
            f"{job_dict['Titel']}\n"
            f"Link: {job_dict['Link']}\n"
            f"Deadline: {job_dict['Frist']}\n"
            f"{job_dict['Veröffentlichungsdatum']}\n"
            f"Arbeitgeber: {job_dict['Ort']}\n"
            f"Nummer: {job_dict['Nummer']}\n"
        ],
        "un": [
            f"- {job_dict['Job Title']}\n"
            f"- {job_dict['Duty Station']}\n"
            f"- Network: {job_dict['Job Network']}\n"
            f"- {job_dict['Department/Office']}\n"
            f"- Deadline: {job_dict['Deadline']}\n"
            f"- Link: {job_dict['Link']}\n"
        ],
        "uniklinik": [
            f"{job_dict['Titel']}\n"
            f"{job_dict['Bereich']}\n"
            f"Frist: {job_dict['Frist']}\n"
            f"{job_dict['Link']}\n"
        ]
    }
    try:
        return "\n".join(structure[mouse])
    except Exception as e:
        return f"Error structuring message: {e}"



def special_treatment(mouse, new_jobs):
    if mouse == "un" and len(new_jobs) > 10:
        message("More than 10 new jobs found. Check the website")
