
import time


def check_frequency(mouse, style, frequency, log):
    # last_checked = log[mouse]
    last_checked = "2025-01-09 16:12:17"  # example
    last_checked = "2025-01-12 23:28:02"
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    now = time.strptime(now, "%Y-%m-%d %H:%M:%S")
    last_checked = time.strptime(last_checked, "%Y-%m-%d %H:%M:%S")

    time_difference = (time.mktime(now) - time.mktime(last_checked))/3600  # hours

    print(time_difference)

    if frequency == "daily":
        if time_difference >= 24:
            return True
    if frequency == "weekly":
        if time_difference >= 24*7:
            return True


check_frequency("test", "hawk", "daily", log={})

