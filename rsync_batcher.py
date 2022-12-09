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


PROCESSED_BASE_DIR =  '/scratch/ms/gb/ukc/era5_processed/%s'
PROCESSED_BASE_DIR_T =  '/scratch/ms/gb/ukc/era5t_processed/%s'
PROCESSED_BASE_DIR_51 =  '/scratch/ms/gb/ukc/era51_processed/%s'

TEMP_FILE_FOLDER = '/scratch/ms/gb/ukc/era5_temp_files/'
TEMP_JOB_FOLDER = '/home/ms/gb/ukc/temp_jobfiles'
CEDA_ARRIVALS_AREAS = {'era5-s-nc':'ecmwf-era5',
                       'era5-s-fc-nc':'ecmwf-era5-fc',
                       'era5-m-nc':'ecmwf-era5-model',
                       'era5-s-en-nc':'ecmwf-era5-en-mem',
                       'era5-s-en-nc-1':'ecmwf-era5-en-mem-1',
                       'era5-s-en-nc-2':'ecmwf-era5-en-mem-2',
                       'era5-s-en-nc-3':'ecmwf-era5-en-mem-3',
                       'era5-s-en-mean-nc':'ecmwf-era5-en-mean',
                       'era5-s-en-sd-nc':'ecmwf-era5-en-mean',
                       'era5t-s-nc':'ecmwf-era5t',
                       'era5t-s-fc-nc':'ecmwf-era5t-fc',
                       'era5t-m-nc':'ecmwf-era5t-model',
                       'era5t-s-en-nc':'ecmwf-era5t-en-mem',
                       'era5t-s-en-mean-nc':'ecmwf-era5t-en-mean',
                       'era5t-s-en-sd-nc':'ecmwf-era5t-en-mean',
                       'era51-s-nc':'ecmwf-era51',
                       'era51-s-fc-nc':'ecmwf-era51-fc',
                       'era51-m-nc':'ecmwf-era51-model',
                       'era51-s-en-nc':'ecmwf-era51-en-mem',
                       'era51-s-en-mean-nc':'ecmwf-era51-en-mean',
                       'era51-s-en-sd-nc':'ecmwf-era51-en-mean',
                       }

EXPECTED_MIN_SIZE = {'era5-m-nc' : {'z':     1200000,
                                   'lnsp':   1500000,
                                    'o3' :  25000000,
                                    'u' :  200000000,
                                    'v' :  200000000,
                                    'vo' : 168000000,
                                    'q':   61000000,
                                    't':   210000000,
                                    },
                      'era5-s-nc':{'10u' : 1500000,
                                   '10v' : 1300000,
                                   '2d' :  1500000,
                                   '2t' :  1500000,
                                   'asn' :  60000,
                                   'cape' : 720000,
                                   'ci' :   150000,
                                   'msl' : 1300000,
                                   'sd' :   60000,
                                   'skt' : 1500000,
                                   'sst' : 900000,
                                   'tcc' : 1250000,
                                   'tcwv': 1400000
                                   },
                      'era5-s-fc-nc':{'metss' :   1100000,
                                      'mntss' :   1100000,
                                      'mslhf' :   1100000,
                                      'msnlwrf' : 1100000,
                                      'msnswrf' :  960000,
                                      'msshf' :   1100000
                                      },
                      'era5-s-en-nc':{'10u' : 1500000,
                                   '10v' : 1300000,
                                   '2d' :  1500000,
                                   '2t' :  1500000,
                                   'asn' :  60000,
                                   'cape' : 720000,
                                   'ci' :   150000,
                                   'msl' : 1300000,
                                   'sd' :   60000,
                                   'skt' : 1500000,
                                   'sst' : 900000,
                                   'tcc' : 1250000,
                                   'tcwv': 1400000
                                   },
                        'era5-s-en-sd-nc':{'10u' : 1500000,
                                   '10v' : 1300000,
                                   '2d' :  1500000,
                                   '2t' :  1500000,
                                   'asn' :  60000,
                                   'cape' : 720000,
                                   'ci' :   150000,
                                   'msl' : 1300000,
                                   'sd' :   60000,
                                   'skt' : 1500000,
                                   'sst' : 900000,
                                   'tcc' : 1250000,
                                   'tcwv': 1400000
                                   },           
                        'era5-s-en-mean-nc':{'10u' : 1500000,
                                   '10v' : 1300000,
                                   '2d' :  1500000,
                                   '2t' :  1500000,
                                   'asn' :  60000,
                                   'cape' : 720000,
                                   'ci' :   150000,
                                   'msl' : 1300000,
                                   'sd' :   60000,
                                   'skt' : 1500000,
                                   'sst' : 900000,
                                   'tcc' : 125000,
                                   'tcwv': 1400000
                                   },}
                      
                      
class ERA5_Rsync_Job:
    """
    Class to prepare ERA5 processing jobs
    """
    
    def __init__(self,stream, qos):
        
        self.stream = stream
        self.qos = qos
        
        if 'era5t' in self.stream:
            
            era5_stream = self.stream.replace('era5t-','era5-')
            
            self.source_dir = PROCESSED_BASE_DIR_T% self.stream
            self.processed_dir =  PROCESSED_BASE_DIR_T% self.stream
            self.expected_size_dict =  EXPECTED_MIN_SIZE[era5_stream]       
        
        elif 'era51' in self.stream:
            
            era5_stream = self.stream.replace('era51-','era5-')
            
            self.source_dir = PROCESSED_BASE_DIR_51% self.stream
            self.processed_dir =  PROCESSED_BASE_DIR_51% self.stream
            self.expected_size_dict =  EXPECTED_MIN_SIZE[era5_stream]       
        
        elif self.stream in ['era5-s-en-nc-1','era5-s-en-nc-2','era5-s-en-nc-3']:
            
            era5_split_stream = self.stream[:-2]
            
            self.source_dir = PROCESSED_BASE_DIR% self.stream
            self.processed_dir =  PROCESSED_BASE_DIR% self.stream
            self.expected_size_dict =  EXPECTED_MIN_SIZE[era5_split_stream]       
        
        
        else:
            self.source_dir = PROCESSED_BASE_DIR% self.stream
            self.processed_dir =  PROCESSED_BASE_DIR% self.stream

            self.expected_size_dict =  EXPECTED_MIN_SIZE[self.stream]       
        self.send_for_transfer()
        self.transfer_dispatcher()
        
        
           

    def send_for_transfer(self):
        """
        Function to check the extraction area for the given stream to see if there
        are any new files there.
        If there are then it will look for file which are over a given modtime age (60s)
        to then send for conversion to netCDF

        """

        full_file_list = glob.glob(os.path.join(self.source_dir,'*.*.nc'))

        self.files_to_send = []
        
        for nc_file in full_file_list:
            
            stats = os.stat(nc_file)
            last_mod_time = stats.st_mtime
            size = stats.st_size
            param = os.path.basename(nc_file).split('.')[-2]

            if time.time() - last_mod_time > 600 and size >= self.expected_size_dict[param]:
                self.files_to_send.append(os.path.basename(nc_file))

    def transfer_dispatcher(self):
        """
        takes a file_list and the stream (ready to pass on in a bit)
        works through these to split into 30 different streams which
        will then be submitted as seperate processes to maxise the available processing 
        """
        
        group_size = len(self.files_to_send) / 10
        remainder = len(self.files_to_send) % 10
        if group_size < 1:
            group_size = 10
            
        while self.files_to_send:
            self.sub_process_id = str(len(self.files_to_send))

            if len(self.files_to_send) > group_size:
                sub_list, self.files_to_send = list(self.files_to_send[0:group_size]), list(self.files_to_send[group_size:])
            else:
                sub_list, self.files_to_send  = list(self.files_to_send[0:]), []
            self._submit_transfer_job(sub_list)
        return
    
    def _submit_transfer_job(self,grib_list):
        
        self.time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_list_file_path = os.path.join(TEMP_FILE_FOLDER,self.stream + '-%s'% self.sub_process_id)
        
        with file(file_list_file_path,'w') as write_file:
            for grib_path in grib_list:
                write_file.write(grib_path+'\n')
        
        self.job_script = list(sl_commands)
        self.job_script.append('#SBATCH --time=00:59:30')       
        
        self.job_script[1] = '#SBATCH --workdir=%s'% self.processed_dir
        
        if self.qos == 'long':
            self.job_script.extend(sl_commands_long)
        elif self.qos == 'large':
            self.job_script.extend(sl_commands_large)
        elif self.qos == 'express':
            self.job_script.extend(sl_commands_express)
        elif self.qos == 'timecrit1':
            self.job_script.extend(sl_commands_timecrit1)

        
        target_dir = CEDA_ARRIVALS_AREAS[stream]
        call_to_make = '$HOME/cronjobs/cronrun.bsh rsync --password-file=/home/ms/gb/ukc/job_templates/common/.rsyncpwd --files-from=%s %s gparton@arrivals.ceda.ac.uk::gparton/%s --port=873 -v --remove-source-files'% (file_list_file_path,self.source_dir,target_dir)
  
              
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
    job = ERA5_Rsync_Job(stream, qos)
    
    
