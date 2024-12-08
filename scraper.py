import os
import re
import json
import asyncio
import pprint
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.error import BadRequest
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Environment variables for API keys and User ID (set in GitHub Secrets)
api_key = '7542268069:AAF7-SuiukANQ9gAhMiRQ51CIGnDRlcCANc'
user_id = '5623557325'


async def send_message(text):
    """Send a message via Telegram."""
    bot = Bot(token=api_key)
    try:
        await bot.send_message(chat_id=user_id, text=text)
    except BadRequest as e:
        print(f"Telegram API Error: {e}")


def get_content(url):
    """Fetch the content for each job posting using Selenium."""
    try:
        # Selenium WebDriver setup
        options = Options()
        options.add_argument("--headless")  # Run in headless mode for GitHub Actions
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        print(f"Fetching content of {url}")

        # Navigate to the job URL
        driver.get(url)

        # Wait for the content to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "li"))
        )

        # Get the page source
        content = driver.page_source
        print("Content fetched successfully.")
        driver.quit()

    except TimeoutException:
        print(f"Timeout loading content for {url}")
        content = "No content found"
    except Exception as e:
        print("Error in get_content:", e)
        content = "No content found"

    return content


def extract_job_infos(content):
    """Extract job information from the fetched content."""
    soup = BeautifulSoup(content, 'lxml')
    listings = soup.find_all('li')
    jobs = []

    for listing in listings:
        if "veröffentlicht" in listing.text:
            try:
                link = "https://www.rwth-aachen.de" + listing.find('a').get('href')
                txt = listing.text
                deadline = txt.split("\n")[3]
                title = txt[:txt.find("[")].replace("\n", "")
                listing_number = re.findall(r'V\d{9}', txt)[0]
                pub_date = re.findall(r'veröffentlicht am \d{2}\.\d{2}\.\d{4}', txt)[0]
                location = txt.split("\n")[2]

                individual_job_dict = {
                    "link": link,
                    "title": title,
                    "listing_number": listing_number,
                    "deadline": deadline,
                    "pub_date": pub_date,
                    'location': location,
                }
                jobs.append(individual_job_dict)
            except Exception as e:
                print(f"Error parsing listing: {e}")

    return jobs


if __name__ == "__main__":
    url = "https://www.rwth-aachen.de/cms/root/Die-RWTH/Arbeiten-an-der-RWTH/~buym/RWTH-Jobportal/?search=&showall=1&aaaaaaaaaaaaanr=&frist=&aaaaaaaaaaaaanq=&aaaaaaaaaaaaany=Einstellung+als+Studentische+Hilfskraft&aaaaaaaaaaaaans=&aaaaaaaaaaaaanw=&aaaaaaaaaaaaanv=&aaaaaaaaaaaaanx="

    # Fetch job content
    content = get_content(url)

    if not content or content == "No content found":
        print("Failed to fetch job content.")
        asyncio.run(send_message("Failed to fetch job content. Something went wrong with Selenium."))
        exit(1)

    # Parse job information
    job_infos = extract_job_infos(content)

    # Compare new jobs with old jobs
    try:
        with open("old_jobs_json.json", "r") as file:
            old_job_infos = json.load(file)
    except FileNotFoundError:
        print("Old jobs file not found, creating a new one.")
        old_job_infos = []

    new_jobs = [job for job in job_infos if job not in old_job_infos]

    # Notify user if new jobs are found
    if new_jobs:
        txt = []
        for job in new_jobs:
            txt.append(
                f"{job['title']}\nLink: {job['link']}\nDeadline: {job['deadline']}\n"
                f"{job['pub_date']}\nArbeitgeber: {job['location']}\nNummer: {job['listing_number']}\n\n"

            )
            txt = "\n".join(txt)
            asyncio.run(send_message(txt))

    # Update the jobs file
    with open("old_jobs_json.json", "w") as file:
        json.dump(job_infos, file, indent=4)
