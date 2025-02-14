import json
import asyncio
from telegram import Bot
from telegram.error import BadRequest

api_key = '7542268069:AAF7-SuiukANQ9gAhMiRQ51CIGnDRlcCANc'
user_ids = ['5623557325']


def problem(mouse, error, send_message=True):
    problem_dict = get_file("logs/problem_logs.json")
    problem_dict[mouse] = f"{problem_dict.get(mouse, '')}, {error}".strip(', ')
    write_file("logs/problem_logs.json", problem_dict)
    if send_message:
        message(f"Error: {error}")


def get_file(name):
    try:
        with open(name, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        problem(mouse=name, error=f"File {name} not found.")
        return []


def write_file(name, content):
    with open(name, "w") as file:
        json.dump(content, file, indent=4)


def to_file(mouse, infos, new, mode):
    if new or infos:
        infos = infos if mouse != "un" else get_file(f"{mode}/{mouse}.json") + new
        write_file(f"{mode}/{mouse}.json", infos)


def configure_text(new, mouse, mode, index, link):
    if mode == "hawk" and new:
        return f"{new} \n{link}"
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
        problem(mouse=mouse, error=f"Error structuring message: {e}")
        return f"Error structuring message: {e}"


def message(txt, test=False):
    async def send_message(text):
        bot = Bot(token=api_key)
        try:
            for user_id in user_ids:
                await bot.send_message(chat_id=user_id, text=text)
        except BadRequest as e2:
            print(f"Telegram API Error: {e2}")
    try:
        if not test:
            asyncio.run(send_message(txt)) if txt else None
    except Exception as e:
        problem(mouse="message", error=f"Error sending message: {e}", send_message=False)
    finally:
        print(txt, end="\n")
