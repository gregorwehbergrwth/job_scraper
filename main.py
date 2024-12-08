import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pprint
import json
import lxml
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import telegram
import asyncio
from telegram.error import BadRequest

api_key = '7542268069:AAF7-SuiukANQ9gAhMiRQ51CIGnDRlcCANc'
user_id = '5623557325'

async def send_message(text):
    bot = telegram.Bot(token=api_key)
    try:
        await bot.send_message(chat_id=user_id, text=text)
    except BadRequest as e:
        print(f"Failed to send message: {e}")



# if __name__ == "__main__":
#     with open("test.txt", "r") as f:
#         text = f.read()
#
#     text = "Nothing"
#
#     print("test")
#
#

def get_content(url):
    """Fetch the content for each job posting using Selenium."""
    try:
        # Selenium WebDriver setup (make sure you have the correct ChromeDriver installed)
        # options = webdriver.ChromeOptions()
        options = Options()

        options.add_argument("--no-default-browser-check")
        options.add_argument("--no-first-run")
        options.add_argument("--disable-default-apps")
        # Define your ChromeDriver path
        # service = Service(r"C:\Users\grego\Downloads\chromedriver-win64_2\chromedriver-win64\chromedriver.exe")
        # service = Service(r"C:\Users\grego\Downloads\chromedriver-win64_3\chromedriver-win64\chromedriver.exe")
        # service = Service(r"C:\Users\grego\Downloads\chromedriver-win64_4\chromedriver-win64\chromedriver.exe")
        # service = Service('chromedriver.exe')  # todo temp
        # driver = webdriver.Chrome(service=service, options=options)  #
        service = Service(ChromeDriverManager().install())

        # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver = webdriver.Chrome(service=service, options=options)

        if True:
            try:

                print(f"Fetching content of {url}")

                # Navigate to the job URL
                driver.get(url)
                #
                # # check for response, alert when none
                # WebDriverWait(driver, 20).until(
                #     EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Expand All')]"))
                # )





                # Get the page source
                content = driver.page_source
                print(content)
            except TimeoutException:
                print(f"Timeout loading content for {url}")
                content = "No content found"
            # break  # Remove or adjust as needed based on your use case

        driver.quit()

    except Exception as e:
        print("Error in get_content:", e)
        content = "No content found"

    return content


def extract_job_infos(content):
    soup = BeautifulSoup(content, 'lxml')
    listings = soup.find_all('li')
    jobs = []

    for listing in listings:
        if "veröffentlicht" in listing.text:
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
    return jobs




if __name__ == "__main__":
    # url = "https://www.rwth-aachen.de/cms/root/die-rwth/arbeiten-an-der-rwth/~buym/rwth-jobportal/?showall=1"
    url = "https://www.rwth-aachen.de/cms/root/Die-RWTH/Arbeiten-an-der-RWTH/~buym/RWTH-Jobportal/?search=&showall=1&aaaaaaaaaaaaanr=&frist=&aaaaaaaaaaaaanq=&aaaaaaaaaaaaany=Einstellung+als+Studentische+Hilfskraft&aaaaaaaaaaaaans=&aaaaaaaaaaaaanw=&aaaaaaaaaaaaanv=&aaaaaaaaaaaaanx="
    content = get_content(url)
    print(content[:300])
    # dump content into textfile
    with open("site_content.txt", "w", encoding='utf-8') as file:
        file.write(content)
    # #

    with open("site_content.txt", "r", encoding='utf-8') as file:
        content = file.read()

    job_infos = extract_job_infos(content)
    # for job in job_infos:
    #     pprint.pprint(job)

    # compare job_infos to the previous job_infos
    # if there are new jobs, send a message to the user
    with open("old_jobs_json.json", "r") as file:
        old_job_infos = json.load(file)

    new_jobs = []
    for index, job in enumerate(job_infos):
        if job not in old_job_infos:
            print(f"New job found: {job['title']}")
            new_jobs.append(job)

    if new_jobs:
        txt = []
        for job in new_jobs:
            txt.append(f"{job['title']}\nLink: {job['link']}\nDeadline: {job['deadline']}\n{job['pub_date']}\nArbeitgeber: {job['location']}\nNummer: {job['listing_number']}\n\n")
        txt = "\n".join(txt)
        asyncio.run(send_message(txt))


    with open("old_jobs_json.json", "w") as file:
        json.dump(job_infos, file, indent=4)

