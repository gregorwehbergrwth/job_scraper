import json


def get_file(name):
    try:
        if name.endswith(".json"):
            with open(name, "r") as file:
                return json.load(file)
        elif name.endswith(".txt"):
            with open(name, "r", encoding="utf-8") as file:
                return file.read()
    except FileNotFoundError:
        print(f"File {name} not found.")
        return "" if name.endswith(".txt") else []


def write_file(name, content):
    if name.endswith(".json"):
        with open(name, "w") as file:
            json.dump(content, file, indent=4)
    elif name.endswith(".txt"):
        with open(name, "w", encoding="utf-8") as file:
            file.write(content)


def to_file(mouse, jobs=None, new_jobs=None, content=None, error=None):
    if new_jobs:
        if mouse == "un":
            jobs = get_file(f"falcon/{mouse}.json")
            jobs.extend(new_jobs)
        write_file(f"falcon/{mouse}.json", jobs)
    elif content:
        # write_file(f"patrol/{mouse}.txt", content)
        write_file(f"hawk/{mouse}.json", content)
    elif error:
        problem_dict = get_file("problematic.json")
        problem_dict.append({mouse: error})
        write_file("problematic.json", content=problem_dict)
