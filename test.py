
job_infos = [0, 1, 3]
# job_infos = []

# old_job_infos = [0, 1, 2]
old_job_infos = []


a = [job for job in job_infos if job not in old_job_infos]

print(a)