import re
from bs4 import BeautifulSoup
import json

def extract_rwth_job_infos(content):
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

def extract_un_job_infos(content):
    jobs = content.split('View Job Description')

    for i, job in enumerate(jobs):
        if "Job ID" not in job:
            jobs.pop(i)

    job_list = []

    for i, job in enumerate(jobs):
        job_dict = {}
        print(job)
        for i, line in enumerate(job.split('\n')):
            try:
                if ":" not in line and line != "":
                    job_dict["Job Title"] = line


                if "Job ID" in line:
                    job_dict["Job ID"] = line.split(":")[-1].strip()
                    job_dict["Link"] = f"https://careers.un.org/jobSearchDescription/{job_dict['Job ID']}?language=en"
                elif "Job Network" in line:
                    job_dict["Job Network"] = line.split(":")[-1].strip()
                elif "Job Family" in line:
                    job_dict["Job Family"] = line.split(":")[-1].strip()
                elif "Category and Level" in line:
                    job_dict["Category and Level"] = line.split(":")[-1].strip()
                elif "Duty Station" in line:
                    job_dict["Duty Station"] = line.split(":")[-1].strip()
                elif "Department/Office" in line:
                    job_dict["Department/Office"] = line.split(":")[-1].strip()
                elif "Date Posted" in line:
                    job_dict["Date Posted"] = line.split(":")[-1].strip()
                elif "Deadline" in line:
                    job_dict["Deadline"] = line.split(":")[-1].strip()
            except Exception as e:
                print(f"Error parsing listing: {e}")
                job_dict = {e}

        job_list.append(job_dict)

    return job_list


def compare_jobs(file, job_infos):
    try:
        with open(file, "r") as file:
            old_job_infos = json.load(file)
    except FileNotFoundError:
        print("Old jobs file not found, creating a new one.")
        old_job_infos = []

    new_jobs = [job for job in job_infos if job not in old_job_infos]
    return new_jobs

def compare_contents(file, new_content):
    try:
        with open(file, "r", encoding="utf-8") as file:
            old_content = file.read()
    except FileNotFoundError:
        print("Old content file not found, creating a new one.")
        old_content = ""
    return old_content == new_content

def extract_main_content(content, mouse):
    soup = BeautifulSoup(content, 'lxml')
    extractors = {
        "lbb": lambda soup: soup.find('div', id='main').find('div', class_='text').text,
        "stb": lambda soup: soup.find('div', class_='listing').text,
        "imb": lambda soup: soup.find('tbody').text,
        "icom": lambda soup: soup.find('div', class_='listing').text,
        "inab": lambda soup: soup.find('div', class_='elementor-section-wrap').text,
        "e3d": lambda soup: soup.find('div', class_='listing').text,
        "iww": lambda soup: soup.find('div', class_='listing').text,
        "ifam": lambda soup: soup.find('div', id="wrapper-2").text,
        "gut": lambda soup: soup.find('tbody').text,
        "gia": lambda soup: soup.find('div', class_='listing').text,
        "isa": lambda soup: soup.find('tbody').text,
        "ucc": lambda soup: soup.find('div', class_='tabs_wrapper tabs_horizontal').text
    }
    return extractors[mouse](soup)
