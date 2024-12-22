# import json
# import random
#
# def remove_one(file):
#     with open(str(file), 'r') as file:
#         old_job_infos = json.load(file)
#
#     # delete one random job
#     random_job = random.choice(old_job_infos)
#     old_job_infos.remove(random_job)
#     if 'title' not in random_job:
#         print(f"Removed job: {random_job['Job ID']}")
#     else:
#         print(f"Removed job: {random_job['title']}")
#
#     with open('jobs/rwth.json', 'w') as file:
#         json.dump(old_job_infos, file, indent=4)
#
#
# remove_one("jobs/rwth.json")
from bs4 import BeautifulSoup


def get_listings(content, mouse):
    soup = BeautifulSoup(content, 'lxml')
    if mouse == "rwth":
        listings = soup.find_all('li')
        return [listing for listing in listings if "veröffentlicht" in listing.text]
    elif mouse == "uniklinik":
        return soup.find_all("div", class_="tx_wsjobs_jobs__job")
    elif mouse == "un":
        return soup.find_all("div", class_="card border-0 ng-star-inserted")
    elif mouse == "trier":
        listings = soup.find_all("div", class_="row articel-list-job-content")
        return [listing for listing in listings if "student" in listing.text.lower()]

def extract_general_job_infos(content, mouse):
    jobs = []
    for listing in get_listings(content, mouse)[:9]:
        temp_dict = {}
        print(listing.prettify())
        for key, function in extractors[mouse].items():
            try:
                temp_dict[key.strip()] = function(listing)
                print(function(listing))
            except Exception as e:
                print(f"Error parsing listing: {e}")
        jobs.append(temp_dict)

    print(jobs)
    return jobs


with open("test.txt", "r") as f:
    content = f.read()

extractors = {
    "trier": {
        "Titel": lambda x: x.find("div", class_="col-md-6 col-01").text.strip(),
        "Arbeitgeber": lambda x: x.find("div", class_="col-md-3 col-01 modal-link").text.strip(),
        "Link": lambda x: f"https://career-service-hochschule-trier.de{x.find("a")["href"]}" if x.find("a")["href"].startswith("/") else x.find("a")["href"],
        "Art": lambda x: "\n".join(x.find("div", class_="col-md-3 col-02").find_all(string=True)),
    }
}

extract_general_job_infos(content, "trier")


