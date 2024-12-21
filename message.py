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
        asyncio.run(send_message(txt))
    except Exception as e:
        print(f"Error sending message: {e}")
    print(txt, end="\n")


def configure_message(job_dict, mouse):
    structure = {
        "rwth": [
            f"{job_dict.get('Titel', 'N/A')}\n"
            f"Link: {job_dict.get('Link', 'N/A')}\n"
            f"Frist: {job_dict.get('Frist', 'N/A')}\n"
            f"{job_dict.get('Veröffentlichungsdatum', 'N/A')}\n"
            f"Arbeitgeber: {job_dict.get('Ort', 'N/A')}\n"
            f"Nummer: {job_dict.get('Nummer', 'N/A')}\n\n"
        ],
        "un": [
            f"- {job_dict.get('Job Title', 'N/A')}\n"
            f"- {job_dict.get('Duty Station', 'N/A')}\n"
            f"- Network: {job_dict.get('Job Network', 'N/A')}\n"
            f"- {job_dict.get('Department/Office', 'N/A')}\n"
            f"- Deadline: {job_dict.get('Deadline', 'N/A')}\n"
            f"- Link: {job_dict.get('Link', 'N/A')}\n"
        ],
        "uniklinik": [
            f"{job_dict.get('Titel', 'N/A')}\n"
            f"{job_dict.get('Bereich', 'N/A')}\n"
            f"Frist: {job_dict.get('Frist', 'N/A')}\n\n"
            f"{job_dict.get('Link', 'N/A')}\n"
        ]
    }
    try:
        return "\n".join(structure[mouse])
    except Exception as e:
        return f"Error structuring message: {e}"


def special_treatment(mouse, new_jobs):
    if mouse == "un" and len(new_jobs) > 10:
        message("More than 10 new jobs found. Check the website")
