from bs4 import BeautifulSoup
import json
import re


def extract_job_infos(site_content, field_mouse):

    getters = {
        "rwth": lambda soup: [listing for listing in soup.find_all('li') if "veröffentlicht" in listing.text],
        "uniklinik": lambda soup: soup.find_all("div", class_="tx_wsjobs_jobs__job"),
        "un": lambda soup: soup.find_all("div", class_="card border-0 ng-star-inserted"),
        "trier": lambda soup: [listing for listing in soup.find_all("div", class_="row articel-list-job-content") if "student" in listing.text.lower()],
        "asta_aachen": lambda soup: [listing for listing in soup.find("ul", class_="job_listings").find_all("li") if listing.find(class_="location") is not None]
    }

    extractors = {
        "uniklinik": {
            "Link": lambda x: "https://www.ukaachen.de" + x.find('a')['href'],
            "Titel": lambda x: x.find('a').text.strip(),
            "Bereich": lambda x: x.find('p').find_all(string=True)[0],
            "Frist": lambda x: x.find('p').find_all(string=True)[1],
            "Frist ": lambda x: x.find_all('p')[1].text
        },
        "rwth": {
            "Link": lambda x: "https://www.rwth-aachen.de" + x.find('a').get('href'),
            "Frist": lambda x: x.text.split("\n")[3],
            "Titel": lambda x: x.text[:x.text.find("[")].replace("\n", ""),
            "Nummer": lambda x: re.findall(r'V\d{9}', x.text)[0],
            "Veröffentlichungsdatum": lambda x: re.findall(r'veröffentlicht am \d{2}\.\d{2}\.\d{4}', x.text)[0],
            "Ort": lambda x: x.text.split("\n")[2]
        },
        "un": {
            "Job Title": lambda x: x.find("h2", class_="font-weight-bold jbOpen_title").text.strip(),
            "Job ID": lambda x: x.find("span", class_="pull-right jbOpen_Id").text.split(" : ")[1].strip(),
            "Job Network": lambda x: x.find("div", class_="card-body").find_all(string=True)[1].split(" : ")[1].strip(),
            "Job Family": lambda x: x.find("div", class_="card-body").find_all(string=True)[3].split(" : ")[1].strip(),
            "Category and Level": lambda x: f'{x.find("div", class_="card-body").find_all(string=True)[5].strip()}, {x.find("div", class_="card-body").find_all(string=True)[9]}',
            "Duty Station": lambda x: x.find("div", class_="card-body").find_all(string=True)[11].split(" : ")[1].strip(),
            "Department/Office": lambda x: x.find("div", class_="card-body").find_all(string=True)[13].split(" : ")[1].strip(),
            "Date Posted": lambda x: x.find("div", class_="card-body").find_all(string=True)[14].split(" : ")[1].strip(),
            "Deadline": lambda x: x.find("div", class_="card-body").find_all(string=True)[15].split(" : ")[1].strip(),
            "Link": lambda x: f'https://careers.un.org/jobSearchDescription/{x.find("span", class_="pull-right jbOpen_Id").text.split(" : ")[1].strip()}?language=en',
        },
        "trier": {
            "Titel": lambda x: x.find("div", class_="col-md-6 col-01").text.strip(),
            "Arbeitgeber": lambda x: x.find("div", class_="col-md-3 col-01 modal-link").text.strip(),
            "Link": lambda x: f'https://career-service-hochschule-trier.de{x.find("a")["href"]}' if x.find("a")["href"].startswith("/") else x.find("a")["href"],
            "Art": lambda x: ", ".join(x.find("div", class_="col-md-3 col-02").find_all(string=True)),
        },
        "asta_aachen": {
            "Titel": lambda x: x.find("div", class_="position").find_all(string=True)[1].strip(),
            "Arbeitgeber": lambda x: x.find("div", class_="company").text.strip(),
            "Ort": lambda x: x.find("div", class_="location").text.strip(),
            "Link": lambda x: x.find("a")["href"],
            "Datum": lambda x: x.find("ul", class_="meta").find("li", class_="date").find("time")["datetime"],
        }
    }

    jobs = []
    for job in getters[field_mouse](BeautifulSoup(site_content, 'lxml')):
        job_dict = {}
        for key, function in extractors[field_mouse].items():
            try:
                job_dict[key.strip()] = function(job)
                print(f'{key}: {job_dict[key.strip()]}')
            except Exception as e:
                print(f'Error parsing listing: {e}')
        jobs.append(job_dict)

    return jobs


def compare_jobs(mouse, job_infos):
    try:
        with open(f"jobs/{mouse}.json", "r") as file:
            old_job_infos = json.load(file)
    except FileNotFoundError:
        print("Old jobs file not found, creating a new one.")
        old_job_infos = []

    return [job for job in job_infos if job not in old_job_infos]


def compare_contents(mouse, new_content):
    part = []
    try:
        with open(f"waiting_for_change/{mouse}.txt", "r", encoding="utf-8") as file:
            old_content = file.read()
    except FileNotFoundError:
        print("Old content file not found, creating a new one.")
        old_content = ""
    if old_content.strip() == new_content.strip():
        print(f"No new content found for {mouse}")
        return None
    else:
        lines = new_content.split("\n")
        for line in lines:
            if line not in old_content and line != "":
                part.append(line)
        print("\n".join(part))
        return "\n".join(part)


def extract_main_content(content, mouse):
    extractors = {
        "lbb": lambda soup: soup.find('div', id='main').find('div', class_='text').text.strip(),
        "stb": lambda soup: soup.find('div', class_='listing').text.strip(),
        "imb": lambda soup: soup.find('tbody').text.strip(),
        "icom": lambda soup: soup.find('div', class_='listing').text.strip(),
        "inab": lambda soup: soup.find('div', class_='elementor-section-wrap').text.strip(),
        "e3d": lambda soup: soup.find('div', class_='listing').text.strip(),
        "iww": lambda soup: soup.find('div', class_='listing').text.strip(),
        "ifam": lambda soup: soup.find('div', id="wrapper-2").text.strip(),
        "gut": lambda soup: soup.find('tbody').text.strip(),
        "gia": lambda soup: soup.find('div', class_='listing').text.strip(),
        "isa": lambda soup: soup.find('tbody').text.strip(),
        "ucc": lambda soup: soup.find('div', class_='tabs_wrapper tabs_horizontal').text.strip(),
        "asta_trier": lambda soup: soup.find('ul', class_="ce-uploads").text.strip(),
    }
    try:
        return extractors[mouse](BeautifulSoup(content, 'lxml'))
    except Exception as e:
        print(f"Error extracting main content: {e}")
        return None


def to_file(mouse, jobs=None, new_jobs=None, content=None):
    if new_jobs:
        if mouse == "un":
            with open(f'jobs/{mouse}.json', "r") as file:
                jobs = json.load(file)
                jobs.extend(new_jobs)
        with open(f'jobs/{mouse}.json', "w") as file:
            json.dump(jobs, file, indent=4)
    elif content:
        with open(f'waiting_for_change/{mouse}.txt', "w", encoding="utf-8") as file:
            file.write(content)
