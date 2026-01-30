from functions.content_scraper import *
from functions.extract import *
from functions.handling import *
from functions.frequency import *
import os


def bird(name, url, mode, test=False, site_count=1):
    print(f"Checking {name} in {mode} mode. Link: {url}")

    for j in range(site_count):
        print(f"Site count: {j+1}/{site_count}")

        url = configure_url(name=name, url=url, index=j)
        html = get_html(link=url, mouse=name, mode=mode)
        infos = extract_infos(html=html, mouse=name, mode=mode)
        new = compare(mouse=name, newscrape=infos, mode=mode)
        print(new)
        texts = configure_texts(new=new, mouse=name, mode=mode, link=url)
        print(texts)
        messages(texts, test)
        to_file(mouse=name, infos=infos, new=new, mode=mode)


if __name__ == "__main__":
    Test = False
    testmouse = "uniklinik"
    testmode = "falcon"

    links = get_file(name="links.json")

    runmode = os.getenv("RUN_MODE", "job")
    print(f"Running in {runmode} mode")

    if Test:
        bird(name=testmouse, url=links[testmode][testmouse]["link"], mode=testmode, test=True, site_count=links[testmode][testmouse].get("site_count", 1))
    else:
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        problematic = get_file(name="logs/problem_logs.json")
        logs = get_file(name="logs/time_log.json")
        logs[now] = {}
        try:
            for style in links.keys():
                for mouse, item in links[style].items():
                    start_time = time.perf_counter()
                    if check(mouse=mouse, log=item, problem_log=problematic, now=now, runmode=runmode):
                        bird(name=mouse, url=item["link"], mode=style)
                        links[style][mouse]["last_checked"] = now
                        logs[now][mouse] = time.perf_counter() - start_time
        except Exception as e:
            problem(mouse="main", error=f"Error in main execution: {e}")
        finally:
            write_file(name="links.json", content=links)
            write_file(name="logs/time_log.json", content=logs)

    quit_driver()
