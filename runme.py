from message import message
from message import *
from content_scraper import get_content
from extract import *

def rwth(url):
    content = get_content(url)

    job_infos = extract_rwth_job_infos(content)

    # Compare new jobs with old jobs
    new_jobs = compare_jobs(file="jobs/rwth_jobs.json", job_infos=job_infos)
    # Notify user if new jobs are found
    if new_jobs:
        for job in new_jobs:
            message(configure_rwth_message(job))

    # Update the jobs file
    with open("jobs/rwth_jobs.json", "w") as file:
        json.dump(job_infos, file, indent=4)

def un(url):
    content = get_content(url, un=True)


    job_infos = extract_un_job_infos(content)

    # Compare new jobs with old jobs
    new_jobs = compare_jobs(file="jobs/un_jobs.json", job_infos=job_infos)

    # Notify user if new jobs are found
    if new_jobs:
        for job in new_jobs:
            message(configure_un_message(job))
        if len(new_jobs) > 10:
            message("More than 10 new jobs found. Check the website")

    # Update the jobs file
    with open("jobs/un_jobs.json", "w") as file:
        json.dump(job_infos, file, indent=4)


def hawk(sites):

    for key, url in sites.items():
        # Fetch job content
        content = get_content(url)

        main_content = extract_main_content(content, key)

        # Compare new content with old content
        if not compare_contents(file=f"{'waiting_for_change'}/{key}_content.txt", new_content=main_content):
            message(f"New content found for {key}:\n{url}")

        # Update the content file
        with open(f"{'waiting_for_change'}/{key}_content.txt", "w", encoding="utf-8") as file:
            file.write(main_content)

if __name__ == "__main__":


    mice ={
        "lbb": r"https://www.lbb.rwth-aachen.de/cms/LBB/Studium/Abschlussarbeiten/~fdxp/Zu-vergebende-Bachelorarbeiten/",
        "stb": r"https://www.stb.rwth-aachen.de/cms/STB/Studium/~ipde/Studien-und-Abschlussarbeiten/",
        "imb": r"https://www.imb.rwth-aachen.de/go/id/bdjfir",
        "icom": r"https://www.icom.rwth-aachen.de/cms/icom/studium/~meft/abschlussarbeiten/?showall=1",
        "inab": r"https://www.inab.rwth-aachen.de/lehre/studien-und-abschlussarbeiten/",
        "e3d": r"https://www.e3d.rwth-aachen.de/cms/E3D/Studium/~iylt/Studentische-Abschlussarbeiten/",
        "iww": r"https://www.iww.rwth-aachen.de/go/id/lyhp?#aaaaaaaaaaaopri",
        "ifam": r"https://www.ifam.rwth-aachen.de/cms/ifam/Studium/~rrihw/Studien-und-Abschlussarbeiten/",
        "gut": r"https://www.gut.rwth-aachen.de/cms/Geotechnik/Studium/~mfvlv/Angebotene-Studien-und-Abschlussarbeite/",
        "gia": r"https://www.gia.rwth-aachen.de/cms/gia/Studium/~zpqtq/Ausgeschriebene-Abschlussarbeiten/",
        "isa": r"https://www.isa.rwth-aachen.de/cms/isa/studium/studien-und-abschlussarbeiten/~sjmd/bachelorarbeiten/",
        "ucc": r"https://international.ucc.edu.gh/exchange-students"
    }

    rwth(url=r"https://www.rwth-aachen.de/cms/root/Die-RWTH/Arbeiten-an-der-RWTH/~buym/RWTH-Jobportal/?search=&showall=1&aaaaaaaaaaaaanr=&frist=&aaaaaaaaaaaaanq=&aaaaaaaaaaaaany=Einstellung+als+Studentische+Hilfskraft&aaaaaaaaaaaaans=&aaaaaaaaaaaaanw=&aaaaaaaaaaaaanv=&aaaaaaaaaaaaanx=")

    hawk(sites=mice)

    un(url=r"https://careers.un.org/jobopening?language=en&data=%257B%2522aoe%2522:%255B%255D,%2522aoi%2522:%255B%255D,%2522el%2522:%255B%255D,%2522ct%2522:%255B%255D,%2522ds%2522:%255B%255D,%2522jn%2522:%255B%255D,%2522jf%2522:%255B%255D,%2522jc%2522:%255B%2522INT%2522%255D,%2522jle%2522:%255B%255D,%2522dept%2522:%255B%255D,%2522span%2522:%255B%255D%257D")
