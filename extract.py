from bs4 import BeautifulSoup
import json
import re


def extract_job_infos(site_content, field_mouse):
    def get_listings(content, mouse):
        soup = BeautifulSoup(content, 'lxml')
        if mouse == "rwth":
            listings = soup.find_all('li')
            return [listing for listing in listings if "veröffentlicht" in listing.text]
        elif mouse == "uniklinik":
            return soup.find_all("div", class_="tx_wsjobs_jobs__job")
        elif mouse == "un":
            listings = re.split(r'View Job Description', content[content.find("Records per Page:") + len("Records per Page:") + 6:])
            return [listing.strip() for listing in listings if "Job ID" in listing]

    def extract_general_job_infos(content, mouse):
        jobs = []
        for listing in get_listings(content, mouse):
            temp_dict = {}
            for key, function in extractors[mouse].items():
                try:
                    temp_dict[key.strip()] = function(listing)
                    print(function(listing))
                except Exception as e:
                    print(f"Error parsing listing: {e}")
            jobs.append(temp_dict)

        print(jobs)
        return jobs

    def extract_un_job_infos(content, mouse):
        job_list = []

        for listing in get_listings(content, mouse):
            job_dict = {}
            for line in listing.split('\n'):
                try:
                    if ":" not in line and line != "":
                        job_dict["Job Title"] = line
                    else:
                        for parameter in ["Job ID", "Job Network", "Job Family", "Category and Level", "Duty Station", "Department/Office", "Date Posted", "Deadline"]:
                            if parameter in line:
                                job_dict[parameter] = line.split(":")[-1].strip()
                except Exception as e:
                    print(f"Error parsing listing: {e}")

            if "Job ID" in job_dict.keys():
                job_dict["Link"] = f"https://careers.un.org/jobSearchDescription/{job_dict['Job ID']}?language=en"

            job_list.append(job_dict)

        return job_list

    extractors = {
        "uniklinik": {
            "Link": lambda listing: "https://www.ukaachen.de" + listing.find('a')['href'],
            "Titel": lambda listing: listing.find('a').text.strip(),
            "Bereich": lambda listing: listing.find('p').find_all(string=True)[0],
            "Frist": lambda listing: listing.find('p').find_all(string=True)[1],
            "Frist ": lambda listing: listing.find_all('p')[1].text
        },
        "rwth": {
            "Link": lambda listing: "https://www.rwth-aachen.de" + listing.find('a').get('href'),
            "Frist": lambda listing: listing.text.split("\n")[3],
            "Titel": lambda listing: listing.text[:listing.text.find("[")].replace("\n", ""),
            "Nummer": lambda listing: re.findall(r'V\d{9}', listing.text)[0],
            "Veröffentlichungsdatum": lambda listing: re.findall(r'veröffentlicht am \d{2}\.\d{2}\.\d{4}', listing.text)[0],
            "Ort": lambda listing: listing.text.split("\n")[2]
        }
    }

    if field_mouse == "rwth" or field_mouse == "uniklinik":
        return extract_general_job_infos(site_content, field_mouse)
    elif field_mouse == "un":
        return extract_un_job_infos(site_content, field_mouse)


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
        "ucc": lambda soup: soup.find('div', class_='tabs_wrapper tabs_horizontal').text
    }
    return extractors[mouse](beautifulsoup)
