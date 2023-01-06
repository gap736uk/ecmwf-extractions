#!/usr/local/apps/python/2.7.12-01/bin/python

import glob
import time
import os
import sys
import subprocess
import datetime
import string

sys.path.append('/home/ukc/ecmwf-extractions/python_controller')
sys.path.append('/home/ukc/ecmwf-extractions/job_templates/common')


from sl_tmp import *
from sltransfer_options_tmp import transfer_commands

stream = 'era5-s-nc'

EXTRACT_BASE_DIR = '/scratch/ukc/era5_extract/%s/'
PROCESSED_BASE_DIR =  '/scratch/ukc/era5_processed/%s'
TEMP_FILE_FOLDER = '/scratch/ukc/era5_temp_files/'
TEMP_JOB_FOLDER = '/home/ukc/temp_jobfiles'
CEDA_ARRIVALS_AREAS = {'era5-s-nc':'ecmwf-era5',
                       'era5-s-fc-nc':'ecmwf-era5-fc',
                       'era5-m-nc':'ecmwf-era5-model',
                       'era5-s-en-nc':'ecmwf-era5-en-mem',
                       'era5-s-en-mean-nc':'ecmwf-era5-en-mean',
                       'era5-s-en-sd-nc':'ecmwf-era5-en-mean'
                       }

class ERA5_Transfer_Job():

    def __init__(self,stream, qos):
        self.stream = stream
        self.qos = qos
        
        self.transfer_dispatcher()
               
    
    def transfer_dispatcher(self):
        
        self.job_script = list(sl_commands)
        
        self.job_script[1] = '#SBATCH --workdir=%s'% PROCESSED_BASE_DIR% self.stream
        if self.qos == 'long':
            self.job_script.extend(sl_commands_long)
        elif self.qos == 'large':
            self.job_script.extend(sl_commands_large)
        elif self.qos == 'express':
            self.job_script.extend(sl_commands_express)
        elif self.qos == 'timecrit1':
            self.job_script.extend(sl_commands_timecrit1)
        
        target_dir = CEDA_ARRIVALS_AREAS[stream]
        self.job_script.extend(rsync_command)
        self.job_script.append(string.replace(transfer_commands, 'TARGET_DIR', target_dir))
        self._writeJobFile()
        self._submitJob()
        
        
        
    def _writeJobFile(self):
        # Open output file to create job
        # Get process ID to create unique filename
        pid = str(os.getpid())
        self.jobfile = os.path.join(TEMP_JOB_FOLDER, self.stream + "_" + pid +".job")
        
        with open(self.jobfile, 'w') as job:
        
            for line in self.job_script:
                job.write(line+"\n")
        
        return "Job file written successfully. See copy at: \n\n%s\n" % self.jobfile
  
    def _submitJob(self):
        os.system('sbatch %s > dev null 2 /dev/null'% self.jobfile)
        return "Job submitted successfully."
    




if __name__ == "__main__":
    
    stream = sys.argv[1]
    qos = 'normal'
    
    if len(sys.argv) > 2:
        qos = sys.argv[2]
    job = ERA5_Transfer_Job(stream, qos)
