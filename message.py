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
    def configure_rwth_message(rwth_dict):
        txt = [
            f"{rwth_dict['Titel']}\n"
            f"Link: {rwth_dict['Link']}\n"
            f"Deadline: {rwth_dict['Frist']}\n"
            f"{rwth_dict['Veröffentlichungsdatum']}\n"
            f"Arbeitgeber: {rwth_dict['Ort']}\n"
            f"Nummer: {rwth_dict['Nummer']}\n\n"
        ]
        txt = "\n".join(txt)
        return txt

    def configure_un_message(un_dict):
        try:
            txt = [
                f"- {un_dict['Job Title']}\n"
                f"- {un_dict['Duty Station']}\n"
                f"- Network: {un_dict['Job Network']}\n"
                f"- {un_dict['Department/Office']}\n"
                f"- Deadline: {un_dict['Deadline']}\n"
                f"- Link: {un_dict['Link']}\n"
            ]
            txt = "\n".join(txt)
        except Exception as e:
            txt = f"Error parsing listing: {e}"
        return txt
    def configure_uniklinik_message(uniklinik_dict):
        txt = [
            f"{uniklinik_dict['Titel']}\n"
            f"{uniklinik_dict['Bereich']}\n"
            f"Frist: {uniklinik_dict['Frist']}\n\n"
            f"{uniklinik_dict['Link']}\n"
        ]
        txt = "\n".join(txt)
        return txt


    if mouse == "rwth":
        return configure_rwth_message(job_dict)
    elif mouse == "un":
        return configure_un_message(job_dict)
    elif mouse == "uniklinik":
        return configure_uniklinik_message(job_dict)


def special_treatment(mouse, new_jobs):
    if mouse == "un" and len(new_jobs) > 10:
        message("More than 10 new jobs found. Check the website")
