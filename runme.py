from functions.content_scraper import *
from functions.extract import *
from functions.handling import *
import time
from functions.frequency import *


def bird(name, url, mode, driver):
    print(f"Checking {name} with {mode} mode. Link: {url}")
    html = get_html(link=url, mouse=name, selenium_driver=driver, mode=mode)
    infos = extract_infos(html=html, mouse=name, mode=mode)
    new = compare(mouse=name, new=infos, mode=mode)
    for i, alert in enumerate(new):
        message(configure_text(new=alert, mouse=name, mode=mode, index=i), link=url)
    to_file(mouse=name, infos=infos, new=new, mode=mode)


if __name__ == "__main__":
    time_logger = {}

    selenium_driver = get_driver()

    links = get_file(name="links.json")
    problematic = get_file(name="logs/problem_logs.json")
    new_log = get_file(name="logs/new_log.json")

    for style in links.keys():
        for mouse in links[style].keys():
            start_time = time.perf_counter()
            # if check_frequency(mouse=mouse, style=style, frequency=links[style][mouse]["frequency"], log=new_log):
            bird(name=mouse, url=links[style][mouse]["link"], driver=selenium_driver, mode=style) if mouse not in problematic.keys() else None
            time_logger[mouse] = time.perf_counter() - start_time

    selenium_driver.quit()

    logs = get_file(name="logs/time_log.json") + [{time.strftime("%Y-%m-%d %H:%M:%S"): time_logger}]
    write_file(name="logs/time_log.json", content=logs)
