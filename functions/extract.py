from bs4 import BeautifulSoup
import re
from functions.handling import get_file
from functions.handling import problem

modes = {
    "falcon": {
        "uniklinik": {
            "table": lambda soup: soup.find_all("div", class_="tx_wsjobs_jobs__job"),
            "lines": {
                "Link": lambda x: "https://www.ukaachen.de" + x.find('a')['href'],
                "Titel": lambda x: x.find('a').text.strip(),
                "Bereich": lambda x: x.find('p').find_all(string=True)[0],
                "Frist": lambda x: x.find('p').find_all(string=True)[1] if len(x.find_all('p')) == 1 else x.find_all('p')[1].text,
            }
        },
        "rwth": {
            "table": lambda soup: [listing for listing in soup.find_all('li') if "veröffentlicht" in listing.text],
            "lines":  {
                "Link": lambda x: "https://www.rwth-aachen.de" + x.find('a').get('href'),
                "Frist": lambda x: f"Frist: {x.text.split("\n")[3]}",
                "Titel": lambda x: x.text[:x.text.find("[")].replace("\n", ""),
                "Nummer": lambda x: re.findall(r'V\d{9}', x.text)[0],
                "Veröffentlichungsdatum": lambda x: re.findall(r"veröffentlicht am \d{2}\.\d{2}\.\d{4}", x.text)[0],
                "Arbeitgeber": lambda x: x.text.split("\n")[2]
            },
        },
        "un": {
            "table": lambda soup: soup.find_all("div", class_="card border-0 ng-star-inserted"),
            "lines": {
                "Job Title": lambda x: x.find("h2", class_="font-weight-bold jbOpen_title").text.strip(),
                "Job ID": lambda x: x.find("span", class_="pull-right jbOpen_Id").text.split(" : ")[1].strip(),
                "Job Network": lambda x: x.find("div", class_="card-body").find_all(string=True)[1].split(" : ")[1].strip(),
                "Job Family": lambda x: x.find("div", class_="card-body").find_all(string=True)[3].split(" : ")[1].strip(),
                "Category and Level": lambda x: f'{x.find("div", class_="card-body").find_all(string=True)[5].strip()}, {x.find("div", class_="card-body").find_all(string=True)[9]}',
                "Duty Station": lambda x: x.find("div", class_="card-body").find_all(string=True)[11].split(" : ")[1].strip(),
                "Department/Office": lambda x: x.find("div", class_="card-body").find_all(string=True)[13].split(" : ")[1].strip(),
                "Date Posted": lambda x: x.find("div", class_="card-body").find_all(string=True)[14].split(" : ")[1].strip(),
                "Deadline": lambda x: f"Deadline: {x.find("div", class_="card-body").find_all(string=True)[15].split(" : ")[1].strip()}",
                "Link": lambda x: f'https://careers.un.org/jobSearchDescription/{x.find("span", class_="pull-right jbOpen_Id").text.split(" : ")[1].strip()}?language=en',
            }
        },
        "trier": {
            "table": lambda soup: [listing for listing in soup.find_all("div", class_="row articel-list-job-content") if "student" in listing.text.lower()],
            "lines": {
                "Titel": lambda x: x.find("div", class_="col-md-6 col-01").text.strip(),
                "Arbeitgeber": lambda x: x.find("div", class_="col-md-3 col-01 modal-link").text.strip(),
                "Link": lambda x: f'https://career-service-hochschule-trier.de{x.find("a")["href"]}' if x.find("a")["href"].startswith("/") else x.find("a")["href"],
                "Art": lambda x: ", ".join(x.find("div", class_="col-md-3 col-02").find_all(string=True)),
            }
        },
        "asta_aachen": {
            "table": lambda soup: [listing for listing in soup.find("ul", class_="job_listings").find_all("li") if listing.find(class_="location") is not None],
            "lines": {
                "Titel": lambda x: x.find("div", class_="position").find_all(string=True)[1].strip(),
                "Arbeitgeber": lambda x: x.find("div", class_="company").text.strip(),
                "Ort": lambda x: x.find("div", class_="location").text.strip(),
                "Link": lambda x: x.find("a")["href"],
                "Datum": lambda x: x.find("ul", class_="meta").find("li", class_="date").find("time")["datetime"],
            }
        }
    },
    "hawk": {
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
}


def extract_infos(html, mouse, mode):
    print(f"Extracting infos from {mouse}")
    jobs = []
    config = modes[mode][mouse]
    soup = BeautifulSoup(html, 'lxml') if html else None

    try:
        if mode == "hawk":
            return config(soup).split("\n")
        else:
            for job in config["table"](soup):
                jobs.append({key: func(job) for key, func in config["lines"].items()})
            return jobs
    except Exception as e:
        problem(mouse=mouse, error=f"Error extracting job infos for {mouse}: {e}")
        return None


def compare(mouse, mode, new):
    print(f"Comparing {mouse}")
    old = get_file(f"{mode}/{mouse}.json")
    try:
        result = [x for x in new if x not in old]
        print(f"Found {len(result)} new jobs/lines for {mouse}")
        return result if mode == "falcon" else ["\n".join(result)]
    except Exception as e:
        problem(mouse=mouse, error=f"Error comparing {mouse}: {e}")
        return []
