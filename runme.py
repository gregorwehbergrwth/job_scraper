import time

from functions.content_scraper import *
from functions.extract import *
from functions.handling import *
from functions.frequency import *
import os
from functions.wohnung import wohnung_zusammenfassung


def bird(name, url, mode, driver, test=False, site_count=1):
    print(f"Checking {name} in {mode} mode. Link: {url}")

    for j in range(site_count):
        print(f"Site count: {j+1}/{site_count}")
        url = re.sub(r'(-Aachen\.1\.0\.1\.\d\.)', lambda m: f"-Aachen.1.0.1.{j}.", url) if name == "wg_gesucht" else url

        html = get_html(link=url, mouse=name, selenium_driver=driver, mode=mode)
        infos = extract_infos(html=html, mouse=name, mode=mode)
        new = compare(mouse=name, newscrape=infos, mode=mode)
        for i, alert in enumerate(new):
            message(configure_text(new=alert, mouse=name, mode=mode, index=i, link=url), test) if not alert.get("blocked", False) else None
        to_file(mouse=name, infos=infos, new=new, mode=mode)


if __name__ == "__main__":
    Test = False
    testmouse = "wg_gesucht"

    run_mode = os.getenv("RUN_MODE", "wg_gesucht")

    now = time.strftime("%Y-%m-%d %H:%M:%S")
    selenium_driver = get_driver() if run_mode == "job" else None

    links = get_file(name="links.json")
    problematic = get_file(name="logs/problem_logs.json")
    logs = get_file(name="logs/time_log.json")
    logs[now] = {}

    for style in links.keys():
        for mouse, item in links[style].items():
            if mouse == testmouse and Test:
                bird(name=mouse, url=item["link"], driver=selenium_driver, mode=style, test=True, site_count=item.get("site_count", 1))
                continue
            elif Test:
                continue
            start_time = time.perf_counter()
            if check(mouse=mouse, log=item, problem_log=problematic):
                bird(name=mouse, url=item["link"], driver=selenium_driver, mode=style)
            links[style][mouse]["last_checked"] = now
            logs[now][mouse] = time.perf_counter() - start_time

    # if run_mode == "wohnung" or Test:
    #     message(wohnung_zusammenfassung())

    write_file(name="links.json", content=links)
    write_file(name="logs/time_log.json", content=logs)
