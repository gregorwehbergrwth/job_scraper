import time


def check(mouse, log, problem_log, now, runmode):
    if (runmode == "job" and mouse == "wg_gesucht") or (runmode == "wohnung" and mouse != "wg_gesucht"):
        return False

    to_time = lambda x: time.mktime(time.strptime(x, "%Y-%m-%d %H:%M:%S"))
    time_difference = (to_time(now) - to_time(log["last_checked"])) / 3600

    frequency_hours = {"instant": 1, "hourly": 1, "daily": 24, "weekly": 24 * 7, "never": 10000}

    return time_difference + 1 >= frequency_hours.get(log["frequency"], None) and mouse not in problem_log.keys()
