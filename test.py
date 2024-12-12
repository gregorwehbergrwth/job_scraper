import json
import random

def remove_one(file):
    with open(str(file), 'r') as file:
        old_job_infos = json.load(file)

    # delete one random job
    random_job = random.choice(old_job_infos)
    old_job_infos.remove(random_job)
    if 'title' not in random_job:
        print(f"Removed job: {random_job['Job ID']}")
    else:
        print(f"Removed job: {random_job['title']}")

    with open('jobs/un_jobs.json', 'w') as file:
        json.dump(old_job_infos, file, indent=4)

# test("jobs/rwth_jobs.json")

remove_one("jobs/un_jobs.json")
