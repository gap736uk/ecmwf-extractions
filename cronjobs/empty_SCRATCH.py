#!/usr/bin/env python

"""
empty_SCRATCH.py
================

Empties old directories that are sitting around in $SCRATCH/

Anything older than 3-hours old is deleted.

"""

# Imports
import os, sys, commands
import time

now=time.time()
threeHours=60*60*3

SCRATCH=os.environ["SCRATCH"]
#quota=commands.getoutput("/usr/local/share/ecquota -v")
quota=[]

for line in quota:
    if line.find("localscratch")>-1:
        items=line.split()
        usage=long(items[1])
        max=long(items[3])*0.9 # 10% safety threshold

dirs=os.listdir(SCRATCH)
print "Deleting old stuff from scratch."

for dir in dirs:
    if dir=="scratchdir" or dir[0]==".": continue
    scr_dir_path(os.path.join(SCRATCH, dir))
    creationTime=os.stat(scr_dir_path)[-1]
    if (now-creationTime)>threeHours and not os.listdir(scr_dir_path):
        comm="rm -Rf %s" % os.path.join(SCRATCH, dir)
        print "Executing:",comm
        os.system(comm)
