#!/usr/local/apps/python/2.7.12-01/bin/python

import glob
import time
import os
import sys
import subprocess
import datetime

sys.path.append('/home/ms/gb/ukc/python_controller')
sys.path.append('/home/ms/gb/ukc/job_templates/common')


from sl_tmp import *

stream = 'era5-s-nc'

EXTRACT_BASE_DIR = '/scratch/ms/gb/ukc/era5_extract_pre_split/%s/'
EXTRACT_BASE_DIR_T = '/scratch/ms/gb/ukc/era5t_extract_pre_split/%s/'
EXTRACT_BASE_DIR_51 = '/scratch/ms/gb/ukc/era51_extract_pre_split/%s/'

PROCESSED_BASE_DIR = '/scratch/ms/gb/ukc/era5_extract/%s/'
PROCESSED_BASE_DIR_T = '/scratch/ms/gb/ukc/era5t_extract/%s/'
PROCESSED_BASE_DIR_51 = '/scratch/ms/gb/ukc/era51_extract/%s/'


TEMP_FILE_FOLDER = '/scratch/ms/gb/ukc/era5_temp_files/'
TEMP_JOB_FOLDER = '/home/ms/gb/ukc/temp_jobfiles'

EXPECTED_MIN_SIZE = {'era5-m-nc' : 1712107200,
                     'era5-s-nc': 26886360,
                      'era5-s-fc-nc':199353600,
                      'era5-s-en-mean-nc':19616880,
                      'era5-s-en-sd-nc': 19616880,            
                      'era5-s-en-nc':196168800,
                      'era5-s-en-nc-1':196168800,
                      'era5-s-en-nc-2':196168800,
                      'era5-s-en-nc-3':196168800,
                       }

class ERA5_Process_Job:
    """
    Class to prepare ERA5 processing jobs
    """
    
    def __init__(self,stream, qos):
        
        self.stream = stream
        self.qos = qos
        
        if 'era5t' in stream:
            
            self.extract_base_dir  = EXTRACT_BASE_DIR_T% self.stream
            era5_stream = self.stream.replace('era5t-','era5-')
            self.expected_size = EXPECTED_MIN_SIZE[era5_stream]
        
        elif 'era51' in stream:
            
            self.extract_base_dir  = EXTRACT_BASE_DIR_51% self.stream
            era5_stream = self.stream.replace('era51-','era5-')
            self.expected_size = EXPECTED_MIN_SIZE[era5_stream]
        
        
        else:
            self.extract_base_dir = EXTRACT_BASE_DIR% self.stream
            self.expected_size = EXPECTED_MIN_SIZE[self.stream] 
            
        self.send_for_splitting()
        self.splitter_dispatcher()
        
        
           

    def send_for_splitting(self):
        """
        Function to check the extraction area for the given stream to see if there
        are any new files there.
        If there are then it will look for file which are over a given modtime age (60s)
        to then send for conversion to netCDF

        """

        full_file_list = glob.glob(os.path.join(self.extract_base_dir,'*.grb'))
        
        self.files_to_split = []
        for grib_file in full_file_list:
            
            stats = os.stat(grib_file)
            last_mod_time = stats.st_mtime
            size = stats.st_size
            
            if time.time() - last_mod_time > 120 and size >= self.expected_size:
                   
                self.files_to_split.append(grib_file)

    def splitter_dispatcher(self):
        """
        takes a file_list and the stream (ready to pass on in a bit)
        works through these to split into 30 different streams which
        will then be submitted as seperate processes to maxise the available processing 
        """
        group_size = len(self.files_to_split) / 25
        remainder = len(self.files_to_split) % 25
        
        if group_size < 1:
            group_size = 25
        while self.files_to_split:
            self.sub_process_id = str(len(self.files_to_split))

            if len(self.files_to_split) > group_size:
                sub_list, self.files_to_split = list(self.files_to_split[0:group_size]), list(self.files_to_split[group_size:])
            else:
                sub_list, self.files_to_split  = list(self.files_to_split[0:]), []
            self._submit_splitter_job(sub_list)
        return
    
    def _submit_splitter_job(self,grib_list):
        
        self.time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_list_file_path = os.path.join(TEMP_FILE_FOLDER,self.stream + '-%s'% self.sub_process_id)
        
        with file(file_list_file_path,'w') as write_file:
            for grib_path in grib_list:
                write_file.write(grib_path+'\n')
        
        self.job_script = list(sl_commands)
        
        if self.qos == 'long':
            self.job_script.extend(sl_commands_long)
        elif self.qos == 'large':
            self.job_script.extend(sl_commands_large)
        elif self.qos == 'express':
            self.job_script.extend(sl_commands_express)
        elif self.qos == 'timecrit1':
            self.job_script.extend(sl_commands_timecrit1)

        
        
        self.job_script.append('#SBATCH --time=00:59:30')
     
        call_to_make =  'python /home/ms/gb/ukc/grib_splitter_call.py %s %s > dev null 2 /dev/null'% (file_list_file_path,stream)
        self.job_script.append(call_to_make)
        
        self._writeJobFile()
        self._submitJob()
        
        
        
    def _writeJobFile(self):
        # Open output file to create job
        # Get process ID to create unique filename
        pid = str(os.getpid())
        self.jobfile = os.path.join(TEMP_JOB_FOLDER, self.stream + "_" + pid + "-" + self.sub_process_id +".job")
        
        with open(self.jobfile, 'w') as job:
        
            for line in self.job_script:
                job.write(line+"\n")
        
        return "Job file written successfully. See copy at: \n\n%s\n" % self.jobfile
  
    def _submitJob(self):
        os.system('sbatch %s > dev null 2 /dev/null'% self.jobfile)
        return "Job submitted successfully."

if __name__ == "__main__":
    
    stream = sys.argv[1]
    qos = 'express'
    if len(sys.argv) > 2:
        qos = sys.argv[2]

    job = ERA5_Process_Job(stream, qos)
    
    
