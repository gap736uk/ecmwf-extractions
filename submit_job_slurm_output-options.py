#!/usr/bin/python3.6

"""

submit_job.py
=============

Python control script for creating and executing MARS jobs
from BADC templates.

Usage:
======

    submit_job.py [-s <YYYYMMDD> | -ago <ndays>] [-e <YYYYMMDD>]
        [-l <levels>] [-p <params>] [-t <times>] [-step <forecast_steps>]
	[-target <target_dir_at_badc>] [-f <file_template>] <dataset> 

Where:
======

    -s		- is the start date (or only date)
    -e 		- is the end date
    -ago	- set date as <ndays> ago. If neither 'start' nor 'end' date
                  provided and 'ago' is not set then the default is 10 days ago.
    -l		- <levels> are the level numbers as a comma-separated list.
    -p		- <params> are the parameter numbers or character codes as a
    		  comma-separated list.
    -t		- <times> are the (analysis) hours required as a comma-separated list.
    -step	- <forecast_steps> are the forecast steps required as a 
    		  comma-separated list.
    -target	- <target_dir_at_badc> is where you want the data to be copied to
    		  at the BADC (on fair!).
    -f		- <file_template> is the template used for naming the output files,
    		  following the MARS conventions.
    <dataset>	- is the dataset ID that you want to extract (e.g. op-2.5-as, op-t159-av,
     		  op-n80r-fs).
    -n          - request for netCDF output
		  

Example usage:
==============

    submit_job.py -s 1999010318 -e 1999020300 op-2.5-as

This will run the Operational 2.5 degree surface analysis job for 
the period of 18:00 on 3rd Jan 1999 until 00:00 on 3rd Feb 1999.

"""

# Import required standard modules
import os
import sys
import string
import re
import time

sys.path.append('/home/ms/gb/ukc/python_controller')
import times 

# Define directory names
basedir="/home/ms/gb/ukc"
templatedir=os.path.join(basedir, "job_templates")
jobdir=os.path.join(basedir, "temp_jobfiles")

sys.path.append(os.path.join(templatedir, 'common'))


# Import commands from local modules
from sl_tmp import sl_commands
from slmkdir_tmp import mkdir_commands
#from sltransfer_tmp import transfer_commands
from sltransfer_options_tmp import convert_commands as transfer_commands
from slrmdir_tmp import rmdir_commands
from slloops_tmp import loop_commands, endloop_commands
from slbadc_dirs import target_dirs


def exitNicely(error=""):
    """
    Nice error message that also prints usage string.
    """
    print(__doc__)
    print("\n",error,"\n")
    sys.exit()


class MarsJob:
  """
  Class to create and execute operational MARS jobs.
  """

  def __init__(self, dataset, kw):
    self.dataset=dataset
    self.dparts=string.split(dataset,"-")
    self.superset=self.dparts[0] 
    self.template=os.path.join(templatedir, self.superset, dataset+".tmp")
    self.job_script=[]  
    if 'target_dir' not in kw.keys():
      self.target_dir=target_dirs[self.dparts[0]+"-"+self.dparts[1]]

    # Set keywords as instance attributes 
    for key in kw.keys():
        setattr(self, key, kw[key])

    # Create a list of dates if keyword 'end' provided
    if hasattr(self, 'end'):
        starttuple=(int(self.start[:4]), int(self.start[4:6]), int(self.start[6:8]))
        endtuple=(int(self.end[:4]), int(self.end[4:6]), int(self.end[6:8])) 
        self.datelist=times.createList(starttuple, endtuple, (1, "day"), listtype="string", formatstring="%Y%m%d")
        #print self.datelist

    # If 'ago' keyword used then calculate the 'start' date
    if hasattr(self, 'ago'):
        self.start=self.getDaysAgo()

    # Run each method
    self.compileParts()
    print(self.writeJobFile())
    self.submitJob()


  def __setattribute__(self, att, value):
    apply(setattr, att, value)
    return    


  def compileParts(self):
    job_info=open(self.template, 'r').readlines()
    """ The following line sucks in commands to :
          1) set up slurm batch process (sl_commands)
          2) set up commands to loop the process (loop_commands)
          3) bring in commands to make directories
          4) have job informaiton  - which is the mars job info
    """
    linelist=sl_commands+["\n"]+loop_commands+["\n"]+mkdir_commands+["\n"]+job_info+["\n"]
    linelist=linelist+[i+"\n" for i in transfer_commands.split("\n")]+["\n"]+rmdir_commands+["\n"]+endloop_commands




    for line in linelist:
        if string.find(line, 'JOB_NAME_HERE')>-1:
            line=string.replace(line, 'JOB_NAME_HERE', self.dataset)
        elif string.find(line, '# NO_LOOPS_IS_DEFAULT')>-1:
	    if hasattr(self, 'datelist'):   
	        dates=""
		loop_comm=""
		# Work out how many variables we should define for dates
		nvars=int(len(self.datelist)/5)
		#vars=[]
		if (len(self.datelist)%5)!=0: nvars=nvars+1
		#print "NCVARS", nvars
		for n in range(0,nvars):
		  s=n*5
		  dates=""
		  for i in range(s,s+5):
		     #print i, n
		     if i==(len(self.datelist)):
		       break
		     else:
  	  	       dates=dates+"%s/" % (self.datelist[i]) 
		  print(dates)
		  loop_comm=loop_comm+"\nV%d='%s'\n" % (n, dates[:-1])
		
		loop_comm=loop_comm+"\nfor DATE in"
		for n in range(0,nvars):  loop_comm=loop_comm+" $V%d" % n
		loop_comm=loop_comm+"\ndo\n"
		line=string.replace(line, '# NO_LOOPS_IS_DEFAULT', loop_comm)	
	    else:
	    	line=string.replace(line, '# NO_LOOPS_IS_DEFAULT', "")	     
        elif string.find(line, 'PUT_DATE_HERE')>-1:
	      if hasattr(self, 'datelist'):
 	        line=string.replace(line, 'PUT_DATE_HERE', "$DATE")
	      else:
                line=string.replace(line, 'PUT_DATE_HERE', self.start)
        elif string.find(line, 'TARGET_DIR')>-1:
            line=string.replace(line, 'TARGET_DIR', self.target_dir)
        elif string.find(line, '# NO_ENDLOOPS_IS_DEFAULT')>-1:
	      if hasattr(self, 'datelist'):
 	        line=string.replace(line, '# NO_ENDLOOPS_IS_DEFAULT', "done")
	      else:
                line=string.replace(line, '# NO_ENDLOOPS_IS_DEFAULT', "")	    
        elif hasattr(self, 'params') and string.find(line, 'param=')>-1:
            params=string.split(self.params, ",")
            params_out=string.join(params, "/")
            line=" param=%s," % params_out
        elif hasattr(self, 'step') and string.find(line, 'step=')>-1:
            steps=string.split(self.step, ",")
            steps_out=string.join(steps, "/")
            line=" step=%s," % steps_out
        elif hasattr(self, 'times') and string.find(line, 'time=')>-1:
            times=string.split(self.times, ",")
            times_out=string.join(times, "/")
            line=" time=%s," % times_out
        elif hasattr(self, 'levels') and string.find(line, 'level=')>-1:
            levels=string.split(self.levels, ",")
            levels_out=string.join(levels, "/")
            line=" level=%s," % levels_out
        elif hasattr(self, 'file_template') and string.find(line, ' target="$WORK/')>-1:
            line=' target="$WORK/'+self.file_template+'"'

        self.job_script.append(line.rstrip())
    return "Job compiled correctly"


  def getDaysAgo(self):
    # Gets the date for the number of days ago and returns it.
    seconds=int(self.ago)*86400
    t=time.time()-seconds
    lt=time.localtime(t)
    return "%.4d%.2d%.2d" % (lt[0],lt[1],lt[2])    


  def writeJobFile(self):
    # Open output file to create job
    # Get process ID to create unique filename
    pid=str(os.getpid())
    self.jobfile=os.path.join(jobdir, dataset+"_"+pid+".job")
    job=open(self.jobfile, 'w')
    for line in self.job_script:
        job.write(line+"\n")
    job.close()
    return "Job file written successfully. See copy at: \n\n%s\n" % self.jobfile


  def submitJob(self):
    #os.system('/usr/local/share/qsub %s' % self.jobfile)
#    os.system('/usr/lpp/LoadL/full/bin/llsubmit %s > /dev/null 2> /dev/null' % self.jobfile)
    os.system('sbatch %s > /dev/null 2> /dev/null' % self.jobfile)
    return "Job submitted successfully."


if __name__=="__main__":
    args=sys.argv
    print("\nExecuting '%s' with arguments: " % args[0], args[1:],"\n")
    if len(args)<2:
       exitNicely("Not enough arguments given.")

    keywords={}
    dataset=args[-1]

    #print args
    for arg in args[1:-1]:
        if arg in ["-s", "-start", "-date"]:
            keywords['start']=args[args.index(arg)+1]
        elif arg in ["-e", "-end"]:
            keywords['end']=args[args.index(arg)+1]
        elif arg in ["-ago"]:
            keywords['ago']=args[args.index(arg)+1]
        elif arg in ["-l", "-level", "-levels", "-levs"]:
            keywords['levels']=args[args.index(arg)+1]
        elif arg in ["-p","-param","-params"]:
            keywords['params']=args[args.index(arg)+1]
        elif arg in ["-step", "-steps"]:	
            keywords['step']=args[args.index(arg)+1]
        elif arg in ["-target"]:
            keywords['target_dir']=args[args.index(arg)+1]
        elif arg in ["-t","-time"]:
            keywords['times']=args[args.index(arg)+1]
        elif arg in ["-n"]:
            keywords['netcdf']=args[args.index(arg)+1]
        elif arg in ["-f","-filename", "-file", "-file_template"]:
            keywords['file_template']=args[args.index(arg)+1]


    if not keywords.has_key('start') and not keywords.has_key('ago'): 
       #exitNicely("No start date or 'ago' argument provided.")
       keywords['ago']='10'
    if not keywords.has_key('netcdf'):
       keywords['netcdf'] = '0' 
    x=MarsJob(dataset, keywords) 
