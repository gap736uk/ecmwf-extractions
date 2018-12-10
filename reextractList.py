#!/usr/local/bin/python

"""

reextractList.py 
================

programme written by G Parton, BADC

programme allows user to submit a list of jobs to MARS system using a list of dates in a file. 

begun 09/01/09

version history
	v1 wrote basic script to open up file with list of dates, take input from command line and submit jobs using submit_jobs.py script.

"""

import os, sys, getopt, re, glob, time
from submit_job import *


class readDateList:
	def __init__(self, dateFile):
	   file = open(dateFile, 'r')
           self.dates = file.readlines()#file.readline().strip().split()


#*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&

if __name__=="__main__":

    argList=sys.argv[1:]

    (args,outputPath)=getopt.getopt(argList, "d:j:t:")

    dateFile = None
    dataset = None
    target = None
    
    for arg, value in args:
	if arg == "-d":
	   dateFile = value
	elif arg == "-j":
	   dataset = value
	elif arg == "-t":
	   target_dir = value
    


    listOfDates = readDateList(dateFile)
    for dateLine in  listOfDates.dates:
        dateElements = dateLine.strip().split()
	print dateElements
	if len(dateElements) > 1 :
        	if len(dateElements[1]) <2 :
			dateElements[1] =  '0'+dateElements[1] 
		if len(dateElements[2]) <2 :
			dateElements[2] =  '0'+dateElements[2]
        	if len(dateElements) == 4 : 
			if len(dateElements[3]) < 2 :
				dateElements[3] =  '0'+dateElements[3]
			if len(dateElements[3]) > 2 :
				dateElements[3] = dateElements[3][0:2]
	
		if len(dateElements) == 3 :
			startDate = dateElements[0] + dateElements[1] + dateElements[2]
		else :
			startDate = dateElements[0] + dateElements[1] + dateElements[2] + dateElements[3]
	else :
		startDate = dateElements[0]
	keywords = {}
	keywords['start'] = startDate 
	keywords['end'] = startDate
	keywords['target_dir'] = target_dir

	#print type(keywords), keywords, dataset
	#MarsJob(dataset, keywords)
	
	os.system(('submit_job.py -s %s -e %s -target %s %s') % (startDate, startDate, target_dir, dataset))
	os.system('sleep 30')