
import launchd



for job in launchd.jobs():
    print(job.label, job.pid, job.properties, job.plistfilename)
