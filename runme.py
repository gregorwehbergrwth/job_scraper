from message import message
from extract import extract_rwth_job_infos
from content_scraper import get_content
import json

def rwth(url):
    content = get_content(url)
    if not content or content == "No content found":
        print("Failed to fetch job content.")
        message("Failed to fetch job content. Something went wrong with Selenium.")
        exit(1)
    job_infos = extract_rwth_job_infos(content)

    # Compare new jobs with old jobs
    try:
        with open("rwth_jobs.json", "r") as file:
            old_job_infos = json.load(file)
    except FileNotFoundError:
        print("Old jobs file not found, creating a new one.")
        old_job_infos = []

    new_jobs = [job for job in job_infos if job not in old_job_infos]

    # Notify user if new jobs are found
    if new_jobs:
        for job in new_jobs:
            txt = [
                f"{job['title']}\n"
                f"Link: {job['link']}\n"
                f"Deadline: {job['deadline']}\n"
                f"{job['pub_date']}\n"
                f"Arbeitgeber: {job['location']}\n"
                f"Nummer: {job['listing_number']}\n\n"
            ]
            txt = "\n".join(txt)
            message(txt)

    # Update the jobs file
    with open("rwth_jobs.json", "w") as file:
        json.dump(job_infos, file, indent=4)

if __name__ == "__main__":

    rwth(url=r"https://www.rwth-aachen.de/cms/root/Die-RWTH/Arbeiten-an-der-RWTH/~buym/RWTH-Jobportal/?search=&showall=1&aaaaaaaaaaaaanr=&frist=&aaaaaaaaaaaaanq=&aaaaaaaaaaaaany=Einstellung+als+Studentische+Hilfskraft&aaaaaaaaaaaaans=&aaaaaaaaaaaaanw=&aaaaaaaaaaaaanv=&aaaaaaaaaaaaanx=")

