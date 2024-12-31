import json


def get_file(name):
    if name.endswith(".json"):
        with open(f"{name}.json", "r") as file:
            return json.load(file)
    elif name.endswith(".txt"):
        with open(f"{name}.txt", "r", encoding="utf-8") as file:
            return file.read()


def write_file(name, content):
    if name.endswith(".json"):
        with open(f"{name}.json", "w") as file:
            json.dump(content, file, indent=4)
    elif name.endswith(".txt"):
        with open(f"{name}.txt", "w", encoding="utf-8") as file:
            file.write(content)


def to_file(mouse, jobs=None, new_jobs=None, content=None, error=None):
    if new_jobs:
        jobs = get_file(f"jobs/{mouse}.json").extend(new_jobs) if mouse == "un" else jobs
        write_file(f"jobs/{mouse}.json", jobs)
    elif content:
        write_file(f"waiting_for_change/{mouse}.txt", content)
    elif error:
        problem_dict = get_file("problematic.json").append({mouse: error})
        write_file("problematic.json", problem_dict)


# def to_file(mouse, jobs=None, new_jobs=None, content=None, error=None):
#     if new_jobs:
#         if mouse == "un":
#             with open(f'jobs/{mouse}.json', "r") as file:
#                 jobs = json.load(file)
#                 jobs.extend(new_jobs)
#         with open(f'jobs/{mouse}.json', "w") as file:
#             json.dump(jobs, file, indent=4)
#     elif content:
#         with open(f'waiting_for_change/{mouse}.txt', "w", encoding="utf-8") as file:
#             file.write(content)
#     elif error:
#         with open("problematic.json", 'r') as file:
#             problem_dict = json.load(file)
#             problem_dict.append({str(mouse): str(error)}) if mouse not in problem_dict else None
#         with open("problematic.json", 'w') as file:
#             json.dump(problem_dict, file, indent=4)
