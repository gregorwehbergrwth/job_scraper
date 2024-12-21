from message import *
from content_scraper import get_content
from extract import *


def falcon(name, url):
    content = get_content(url, mouse=name)
    print(content)
    if not content:
        message(f"Error fetching content for {url}")
        return
    job_infos = extract_job_infos(content, field_mouse=name)
    new_jobs = compare_jobs(file=f"jobs/{name}.json", job_infos=job_infos)
    with open(f"jobs/{name}.json", "w") as file:
        json.dump(job_infos, file, indent=4)

    print(new_jobs)
    input()
    if new_jobs:
        for job in new_jobs:
            message(configure_message(job, mouse=name))

    special_treatment(mouse=name, new_jobs=new_jobs)
    return len(new_jobs)


def hawk(sites):
    mice_count = 0
    for key, url in sites.items():
        content = get_content(url, mouse=key)
        main_content = extract_main_content(content, key)
        part = compare_contents(file=f"{'waiting_for_change'}/{key}_content.txt", new_content=main_content)
        if part:
            message(f"New content found for {key}:\n{url}\n{part}")
            mice_count += 1
        with open(f"{'waiting_for_change'}/{key}_content.txt", "w", encoding="utf-8") as file:
            file.write(main_content)
    return mice_count


if __name__ == "__main__":

    mice = {
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

    rwth = falcon(name="rwth", url=r"https://www.rwth-aachen.de/cms/root/Die-RWTH/Arbeiten-an-der-RWTH/~buym/RWTH-Jobportal/?search=&showall=1&aaaaaaaaaaaaanr=&frist=&aaaaaaaaaaaaanq=&aaaaaaaaaaaaany=Einstellung+als+Studentische+Hilfskraft&aaaaaaaaaaaaans=&aaaaaaaaaaaaanw=&aaaaaaaaaaaaanv=&aaaaaaaaaaaaanx=")
    un = falcon(name="un", url=r"https://careers.un.org/jobopening?language=en&data=%257B%2522aoe%2522:%255B%255D,%2522aoi%2522:%255B%255D,%2522el%2522:%255B%255D,%2522ct%2522:%255B%255D,%2522ds%2522:%255B%255D,%2522jn%2522:%255B%255D,%2522jf%2522:%255B%255D,%2522jc%2522:%255B%2522INT%2522%255D,%2522jle%2522:%255B%255D,%2522dept%2522:%255B%255D,%2522span%2522:%255B%255D%257D")
    uniklinik = falcon(name="uniklinik", url=r"https://www.ukaachen.de/stellenangebote/stellenmarkt/offene-stellen/?tx_wsjobs_jobs%5Bgroup%5D=12&cHash=dee34d2e821b77aab8fd548eac958bed")
    mice = hawk(sites=mice)

    # if any([rwth, un, mice]):
    #     for key, value in locals().items():
    #         if isinstance(value, int):
    #             message(f"{value} new jobs found for {key}")
