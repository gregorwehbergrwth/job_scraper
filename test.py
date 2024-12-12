import json
import random

with open("jobs/rwth_jobs.json", 'r') as file:
    old_job_infos = json.load(file)

# delete one random job
random_job = random.choice(old_job_infos)
old_job_infos.remove(random_job)
print(f"Removed job: {random_job['title']}")

with open("jobs/rwth_jobs.json", 'w') as file:
    json.dump(old_job_infos, file, indent=4)

