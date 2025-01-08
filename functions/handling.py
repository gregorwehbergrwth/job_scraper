import json


def get_file(name):
    try:
        with open(name, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {name} not found.")
        return []


def write_file(name, content):
    with open(name, "w") as file:
        json.dump(content, file, indent=4)


def to_file(mouse, infos=None, new=None, error=None, mode=None):
    if new:
        if mouse == "un":
            infos = get_file(f"{mode}/{mouse}.json")
            infos.extend(new)
        write_file(f"{mode}/{mouse}.json", infos)
    elif error:
        problem_dict = get_file("problematic.json")
        problem_dict.append({mouse: error})
        write_file("problematic.json", content=problem_dict)
