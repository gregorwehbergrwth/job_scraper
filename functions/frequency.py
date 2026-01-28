import time


def check(mouse, log, problem_log, now, runmode):
    to_time = lambda x: time.mktime(time.strptime(x, "%Y-%m-%d %H:%M:%S"))
    time_difference = (to_time(now) - to_time(log["last_checked"])) / 3600

    frequency_hours = {"instant": 1 / 100, "hourly": 1, "daily": 24, "weekly": 24 * 7, "never": 10000}

    print(f"Checking frequency for {mouse} in {runmode}")
    if runmode == "job" and mouse == "wg_gesucht":
        print(f"blocked {mouse} in {runmode} mode because no wg_gesucht allowed")
        return False
    elif runmode == "wohnung" and mouse != "wg_gesucht":
        print(f"blocked {mouse} in {runmode} mode because only wg_gesucht allowed")
        return False
    elif mouse in problem_log.keys():
        print(f"blocked {mouse} because it is in problem log")
        return False
    elif time_difference <= frequency_hours.get(log["frequency"], None):
        print(f"blocked {mouse} because frequency limit not reached: {time_difference} hours since last check, needs {frequency_hours.get(log['frequency'], None)} hours")
        return False
    else:
        print(f"allowed {mouse} to run: {time_difference} hours since last check, needs {frequency_hours.get(log['frequency'], None)} hours")
        return True
