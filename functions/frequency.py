import time


def check(mouse, log, problem_log, now):

    now = time.strptime(now, "%Y-%m-%d %H:%M:%S")
    last_checked = time.strptime(log["last_checked"], "%Y-%m-%d %H:%M:%S")

    time_difference = (time.mktime(now) - time.mktime(last_checked)) / 3600

    frequency_hours = {"fourminutely": 1/15, "fiveminutely": 1/12, "hourly": 1, "daily": 24, "weekly": 24 * 7, "never": 10000}

    return time_difference + 1 >= frequency_hours.get(log["frequency"], None) and mouse not in problem_log.keys()
