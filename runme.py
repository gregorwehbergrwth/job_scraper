from message import *
from content_scraper import get_content
from extract import *


def falcon(name, url):
    content = get_content(url, mouse=name)
    if not content:
        message(f"Error fetching content for {url}")
        return
    job_infos = extract_job_infos(content, field_mouse=name)
    new_jobs = compare_jobs(file=f"jobs/{name}.json", job_infos=job_infos)
    if new_jobs:
        to_file(job_infos, new_jobs, name)
        for job in new_jobs:
            message(configure_message(job, mouse=name))
        special_treatment(mouse=name, new_jobs=new_jobs)


def hawk(key, url):
    content = get_content(url, mouse=key)
    if not content:
        message(f"Error fetching content for {url}")
        return
    main_content = extract_main_content(content, key)
    part = compare_contents(file=f"waiting_for_change/{key}_content.txt", new_content=main_content)
    if part:
        message(f"New content found for {key}:\n{url}\n{part}")
        to_file(main_content, new_content=None, mouse=key)


if __name__ == "__main__":
    with open("links.json", 'r') as file:
        links = json.load(file)
    for prey, link in links["prey"].items():
        falcon(name=prey, url=link)
    for mouse, link in links["mice"].items():
        hawk(mouse, link)
