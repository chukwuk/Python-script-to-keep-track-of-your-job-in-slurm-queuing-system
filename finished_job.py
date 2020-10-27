import os
import time, threading

#This script is meant to check the jobs on the queue and update the ones that finish running.  It does this by generating a text file every so often that contains the output of 'qstat -u username'.  The program stores the jobs that are running in an array, then the next time update the program makes another text file, stores the running jobs in an array, and checks to see which jobs from before are no longer running.  These are the jobs that have finished and need to be updated in some way.


cwd = os.getcwd()
#username = 'chukwuk'
username = input("Please enter your username: ")

global jobs_0
jobs_0 = []
global jobs_0_ID
jobs_0_ID = []
global job_paths
job_paths = []
global jobs_1
jobs_1 = []
global jobs_1_ID
jobs_1_ID = []
global job_names
job_names = []


updates_paths = []
updates_names = []


def get_current_jobs():
  if not os.path.exists(cwd + '/current_jobs'):
    print ('Creating text file for current jobs')
    os.system('squeue -u ' + username + ' > current_jobs')
    with open(os.path.join(cwd + '/current_jobs')) as myFile:
      for num, line in enumerate(myFile, 1):
        jobs_0.append(line)
        numlines_0 = num
        if num > 1:
          splitline = line.split()
          jobs_0_ID.append(splitline[0])
    print ('Getting ID values for current jobs')
    get_job_paths(jobs_0_ID)
    print ('Writing text file for job paths')
    file = open('job_paths', 'w')
    for paths in job_paths:
      file.write(paths + '\n')
    file.close()
    print ('Writing text file for job names')
    file = open('job_names', 'w')
    for names in job_names:
      file.write(names + '\n')
    file.close()
  else:
    print ("current_jobs folder already exists - don't overwrite - just read text files")
    with open(os.path.join(cwd + '/current_jobs')) as myFile:
      for num, line in enumerate(myFile, 1):
        jobs_0.append(line)
        numlines_0 = num
        if num > 1:
          splitline = line.split()
          jobs_0_ID.append(splitline[0])
    with open(os.path.join(cwd + '/job_paths')) as myFile:
      for num, line in enumerate(myFile, 1):
        job_paths.append(line)
    with open(os.path.join(cwd + '/job_names')) as myFile:
      for num, line in enumerate(myFile, 1):
        job_names.append(line)
        

def get_new_jobs():
  os.system('squeue -u ' + username + ' > new_jobs')
  with open(os.path.join(cwd + '/new_jobs')) as myFile:
    for num, line in enumerate(myFile, 1):
      jobs_1.append(line)
      numlines_0 = num
      if num > 1:
        splitline = line.split()
        jobs_1_ID.append(splitline[0])
        


def get_job_paths(job_array):
  for jobs in job_array:
    temp_string = 'scontrol show job ' + str(jobs) +'| grep WorkDir'+ ' > temp_job'
    os.system(temp_string)
    with open(os.path.join(cwd + '/temp_job')) as myFile:
      for num, line in enumerate(myFile, 1):
        if 'WorkDir' in line:
          tline = line.strip()
          splitline = tline.split('=')
          job_paths.append(splitline[1])
    temp_string_1 = 'scontrol show job ' + str(jobs) +'| grep JobName'+ ' > temp_job_1'
    os.system(temp_string_1)
    with open(os.path.join(cwd + '/temp_job_1')) as myFile_1:
      for num, line in enumerate(myFile_1, 1):
        if 'JobName' in line:
          tline = line.strip()
          splitline = tline.split()
          splitline_1 = splitline[1].split('=')
          job_names.append(splitline_1[1])
  os.system('rm -rf temp_job')
  os.system('rm -rf temp_job_1')



def timer():
    print(time.ctime())
    
    get_new_jobs()
    
    updates = set(jobs_0_ID) - set(jobs_1_ID)
    
    print (updates)
    get_job_paths(updates)
    for path in job_paths:
      print (path)
    
    threading.Timer(100, timer).start()
    

#_________________________________________________________________________________________________________________________________________________________________________________________________________
#Start the timer program
#timer ()





get_current_jobs()
get_new_jobs()
    
updates = set(jobs_0_ID) - set(jobs_1_ID)

if updates == set([]):
  print ('no updates yet')
else:
  print (updates)
  for jobs in updates:
    index = jobs_0_ID.index(jobs)
    updates_paths.append(job_paths[index])
    updates_names.append(job_names[index])
  #print(job_paths)
  print ("These are the paths that have finished and need to be updated")
  for path in updates_paths:
    print (path)
  print ("These are the names of the jobs that have finished")
  for name in updates_names:
    print (name)
  file = open('job_updates', 'w')
  for names in updates_names:
    index = updates_names.index(names)
    file.write(names + '\n')
    file.write(updates_paths[index] + '\n')
    file.write('\n')
  file.close()





