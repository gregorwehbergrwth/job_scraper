import json
import asyncio
from telegram import Bot
from telegram.error import BadRequest
import re

api_key = '8030882097:AAHyDEN1DWhyRYUhbUOBA8b-Gz0AIpOEJlg'
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
        infos = infos if mouse not in ["un", "wg_gesucht"] else get_file(f"{mode}/{mouse}.json") + new
        write_file(f"{mode}/{mouse}.json", infos)


def configure_text(new, mouse, mode, index, link):
    if mode == "hawk":
        return f"{new} \n{link}" if new else None
    else:
        job_dict = new

    structure = {
        "uniklinik": ['Titel', 'Bereich', 'Frist', 'Link'],
        "rwth": ['Titel', 'Frist', 'Veröffentlichungsdatum', 'Arbeitgeber', 'Link'],
        "un": ['Job Title', 'Duty Station', 'Job Network', 'Department/Office', 'Deadline', 'Link'],
        "trier": ['Titel', 'Arbeitgeber', 'Art', 'Link'],
        "asta_aachen": ['Titel', 'Arbeitgeber', 'Ort', 'Datum', 'Link'],
        "wg_gesucht": ['title', 'price', 'description', 'url']
    }

    try:
        text = "\n".join([job_dict.get(key, 'N/A') for key in structure[mouse]])

        text += "\nMore than 10 new jobs found.\nCheck the website!\n" if index == 9 and mouse == "rwth" else ""
        return text
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


def blocked(mouse, alert):
    if mouse != "wg_gesucht":
        return False

    blockwords = [
        "kathol",
        "verbindung",
        "evangenl",
        "bursche"
    ]

    blocked_addresses = [
        "Lousbergstraße 44",
        "Lousbergstraße 46",
        "Turmstraße 4",
        "Krefelder Straße 24",
        "Krefelder Straße 33",
        "Muffeter Weg 15",
        "Salvatorstraße 38",
        "Am Weißenberg 48",
        "Hainbuchenstraße 23",
        "Salierallee 48",
        "Lütticher Straße 162",
        "Melatener Straße 41",
        "Melatener Straße 48",
        "Moreller Weg 64",
        "Kaiser-Friedrich-Allee 5",
        "Nizzaallee 4",
        "Nizzaallee 56",
        "Junkerstraße 68",
        "Rütscherstraße 110",
        "Kruppstraße 8",
        "Kruppstraße 9",
        "Kruppstraße 10",
        "Kruppstraße 12",
        "Ludwigsallee 101",
        "Hexenberg 10",
        "Försterstraße 10"
    ]

    umlaut_map = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "ß": "ss",
    }

    def normalize_text(text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"\.|\s+", "", text)

        for umlaut, ascii_ in umlaut_map.items():
            text = text.replace(umlaut, ascii_)

        text = re.sub(r"str", "strasse", text) if "strasse" not in text else text

        return text

    blocked_addresses_normalized = [normalize_text(addr) for addr in blocked_addresses]

    if any(bw in alert.get("title", "").lower() for bw in blockwords):
        print(f"Blocked listing (blockwords): {alert.get('title')}")
        return True
    elif normalize_text(alert.get("street", "")) in blocked_addresses_normalized:
        print(f"Blocked listing (address): {alert.get('street')}")
        return True
    else:
        return False


def configure_url(name, url, index):
    return re.sub(r'(-Aachen\.1\.0\.1\.\d\.)', lambda m: f"-Aachen.1.0.1.{index}.", url) if name == "wg_gesucht" else url
