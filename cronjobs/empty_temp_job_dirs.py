#!/usr/bin/env python

"""
empty_temp_job_dirs.py
======================

If there are more than 250 files in either of the following dirs
this job deletes those files.

~/loadleveler_output 
~/temp_jobfiles

"""

import os, sys
import glob
import time
minTime = 25 * 60 * 60 
homeDir="/home/ms/gb/ukc/"

dirs=("slurm_output","loadleveler_output", "temp_jobfiles")

filesToList = "*"

for dir in dirs:
    os.chdir(homeDir + dir)
    if dir == "temp_jobfiles" : filesToList = filesToList + ".job"
   
    files=glob.glob(filesToList)

    for file in files:
       modTime = os.stat(homeDir + dir + '/' + file)
       if time.time() - modTime.st_mtime > minTime:
        
            os.unlink(os.path.join(homeDir, dir, file))
            
		
