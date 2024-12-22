from bs4 import BeautifulSoup
import json
import re


def extract_job_infos(site_content, field_mouse):
    def get_listings(content, mouse):
        soup = BeautifulSoup(content, 'lxml')
        if mouse == "rwth":
            return [listing for listing in soup.find_all('li') if "veröffentlicht" in listing.text]
        elif mouse == "uniklinik":
            return soup.find_all("div", class_="tx_wsjobs_jobs__job")
        elif mouse == "un":
            return soup.find_all("div", class_="card border-0 ng-star-inserted")
        elif mouse == "trier":
            listings = soup.find_all("div", class_="row articel-list-job-content")
            return [listing for listing in listings if "student" in listing.text.lower()]

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
            "Category and Level": lambda x: f"{x.find("div", class_="card-body").find_all(string=True)[5].strip()}, {x.find("div", class_="card-body").find_all(string=True)[9]}",
            "Duty Station": lambda x: x.find("div", class_="card-body").find_all(string=True)[11].split(" : ")[1].strip(),
            "Department/Office": lambda x: x.find("div", class_="card-body").find_all(string=True)[13].split(" : ")[1].strip(),
            "Date Posted": lambda x: x.find("div", class_="card-body").find_all(string=True)[14].split(" : ")[1].strip(),
            "Deadline": lambda x: x.find("div", class_="card-body").find_all(string=True)[15].split(" : ")[1].strip(),
            "Link": lambda x: f"https://careers.un.org/jobSearchDescription/{x.find("span", class_="pull-right jbOpen_Id").text.split(" : ")[1].strip()}?language=en",
        },
        "trier": {
            "Titel": lambda x: x.find("div", class_="col-md-6 col-01").text.strip(),
            "Arbeitgeber": lambda x: x.find("div", class_="col-md-3 col-01 modal-link").text.strip(),
            "Link": lambda x: f"https://career-service-hochschule-trier.de{x.find("a")["href"]}" if x.find("a")["href"].startswith("/") else x.find("a")["href"],
            "Art": lambda x: "\n".join(x.find("div", class_="col-md-3 col-02").find_all(string=True)),
        }
    }

    jobs = []
    for job in get_listings(site_content, field_mouse):
        job_dict = {}
        for key, function in extractors[field_mouse].items():
            try:
                job_dict[key.strip()] = function(job)
                print(job_dict[key.strip()])
            except Exception as e:
                print(f"Error parsing listing: {e}")
        jobs.append(job_dict)

    return jobs


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
    part = []
    try:
        with open(file, "r", encoding="utf-8") as file:
            old_content = file.read()
    except FileNotFoundError:
        print("Old content file not found, creating a new one.")
        old_content = ""
    if old_content == new_content:
        print("None")
        return None
    else:
        lines = new_content.split("\n")
        for line in lines:
            if line not in old_content and line != "":
                part.append(line)
        print("\n".join(part))
        return "\n".join(part)


def extract_main_content(content, mouse):
    beautifulsoup = BeautifulSoup(content, 'lxml')
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
        "ucc": lambda soup: soup.find('div', class_='tabs_wrapper tabs_horizontal').text,
        "asta_trier": lambda soup: soup.find('ul', class_="ce-uploads").text,
    }
    return extractors[mouse](beautifulsoup)


def to_file(content, new_content=None, mouse=None):
    if mouse == "un":
        with open(f"jobs/{mouse}.json", "r+") as file:
            jobs = json.load(file)
            file.seek(0)
            json.dump(jobs.update(new_content), file, indent=4)
    elif not new_content:
        with open(f"waiting_for_change/{mouse}_content.txt", "w", encoding="utf-8") as file:
            file.write(content)
    else:
        with open(f"jobs/{mouse}.json", "w") as file:
            json.dump(content, file, indent=4)
