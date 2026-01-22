from functions.content_scraper import *
from functions.extract import *
from functions.handling import *
from functions.frequency import *


def bird(name, url, mode, driver, test=False):
    print(f"Checking {name} in {mode} mode. Link: {url}")

    # site_count = 1

    url_base = "https://www.wg-gesucht.de/wg-zimmer-in-Aachen.1.0.1.0.html?offer_filter=1&city_id=1&sort_order=0&noDeact=1&categories%5B%5D=0&rMax=500&pagination=1&pu="
    # for j in range(site_count):
    #     url = re.sub(r'(-Aachen\.1\.0\.1\.0\.)', lambda m: f"-Aachen.1.0.1.{j}.", url_base)


    if mode != "buzzard":
        site_count = 1
    else:
        site_count = 1

        for j in range(site_count):
            url = re.sub(r'(-Aachen\.1\.0\.1\.0\.)', lambda m: f"-Aachen.1.0.1.{j}.", url_base) if mode == "buzzard" else url

            html = get_html(link=url, mouse=name, selenium_driver=driver, mode=mode)
            infos = extract_infos(html=html, mouse=name, mode=mode)
            new = compare(mouse=name, new=infos, mode=mode)
            for i, alert in enumerate(new):
                message(configure_text(new=alert, mouse=name, mode=mode, index=i, link=url), test)
            to_file(mouse=name, infos=infos, new=new, mode=mode)
    # else:
    #
    #         html = get_html(link=url, mouse=name, selenium_driver=driver, mode=mode)
    #         infos = extract_infos(html=html, mouse=name, mode=mode)
    #         new = compare(mouse=name, new=infos, mode=mode)
    #         for i, alert in enumerate(new):
    #             message(configure_text(new=alert, mouse=name, mode=mode, index=i, link=url), test)
    #         to_file(mouse=name, infos=infos, new=new, mode=mode)



if __name__ == "__main__":
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    selenium_driver = get_driver()

    links = get_file(name="links.json")
    problematic = get_file(name="logs/problem_logs.json")
    logs = get_file(name="logs/time_log.json")
    logs[now] = {}
    Test = True

    for style in links.keys():
        for mouse, item in links[style].items():
            if mouse == "wg_gesucht" and Test:
                bird(name=mouse, url=item["link"], driver=selenium_driver, mode=style, test=True)
                continue
            elif Test:
                continue
            start_time = time.perf_counter()
            if check(mouse=mouse, log=item, problem_log=problematic):
                bird(name=mouse, url=item["link"], driver=selenium_driver, mode=style)
            links[style][mouse]["last_checked"] = now
            logs[now][mouse] = time.perf_counter() - start_time

    write_file(name="links.json", content=links)
    write_file(name="logs/time_log.json", content=logs)
