from message import *
from content_scraper import *
from extract import *


def falcon(name, url):
    content = get_content(url, mouse=name)
    job_infos = extract_job_infos(content, field_mouse=name) if content else []
    new_jobs = compare_jobs(mouse=name, job_infos=job_infos) if job_infos else []
    to_file(mouse=name, jobs=job_infos, new_jobs=new_jobs)
    for job in new_jobs:
        message(configure_message(job, mouse=name))
    special_treatment(mouse=name, new_jobs=new_jobs)


def hawk(name, url):
    content = get_content(url, mouse="hawk")
    main_content = extract_main_content(content, name) if content else ""
    part = compare_contents(mouse=name, new_content=main_content) if main_content else ""
    to_file(mouse=name, content=main_content)
    # if part:
    #     message(f"{part}\n{url}")


if __name__ == "__main__":
    with open("links.json", 'r') as file:
        links = json.load(file)
    # for prey, link in links["prey"].items():
    #     falcon(name=prey, url=link)
    for mouse, link in links["mice"].items():
        hawk(mouse, link)
