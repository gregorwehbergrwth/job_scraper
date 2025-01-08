from functions.message import *
from functions.content_scraper import *
from functions.extract import *
from functions.handling import *
import time


def bird(name, url, mode, driver):
    content = get_content(link=url, mouse=name, selenium_driver=driver, mode=mode)
    infos = extract_content(site_content=content, field_mouse=name, mode=mode)
    new = compare(mouse=name, new=infos, mode=mode)

    if mode == "falcon":
        to_file(mouse=name, infos=infos, new=new, mode=mode)
        for job in new:
            message(configure_message(job, mouse=name))
        special_treatment(mouse=name, new_jobs=new)
    elif mode == "hawk":
        to_file(mouse=name, infos=infos, new=new, mode=mode)
        if new:
            new = "\n".join(new)  # temp
            message(f"{new}\n{url}")  # todo configure message


if __name__ == "__main__":
    time_logger = {}

    start_time = time.perf_counter()
    selenium_driver = get_driver()
    time_logger["driver"] = time.perf_counter() - start_time

    start_time = time.perf_counter()
    links = get_file(name="links.json")
    problematic = get_file(name="problematic.json")
    time_logger["files"] = time.perf_counter() - start_time


    for style in links.keys():
        for mouse, link in links[style].items():
            start_time = time.perf_counter()
            bird(name=mouse, url=link, driver=selenium_driver, mode=style)
            time_logger[mouse] = time.perf_counter() - start_time

    selenium_driver.quit()

    logs = get_file(name="time_logs/time_log.json")
    logs.append({time.strftime("%Y-%m-%d %H:%M:%S"): time_logger})
    write_file(name="time_logs/time_log.json", content=logs)

