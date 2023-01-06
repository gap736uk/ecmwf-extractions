#!/usr/bin/python3.6

import subprocess
import datetime
import os
import sys
import submit_job_rsync_netcdf_era5_new

streams = ['era5-m-nc',
           #'era5-s-en-mean-nc',
           #'era5-s-en-nc',
           #'era5-s-en-sd-nc',
           #'era5-s-fc-nc',
           #'era5-s-nc'
           ]

base_path = "/home/ms/gb/ukc/era5_control"

backlog_job_file = 'submitted_backlog_runs.txt'


def cmd_line_finder(file_path, test=0):
    with open(file_path, 'r+') as f: #open in read / write mode
            
                    
        line = f.readline() #read the first line and throw it out
        data = f.read() #read the rest
        if not test:
            f.seek(0) #set the cursor to the top of the file
            f.write(data) #write the data back
            f.truncate() #set the file size to the current size

        return line

   

if __name__=="__main__":

    args = sys.argv
    print("\nExecuting '%s' with arguments: " % args[0], args[1:],"\n")
    if len(args) < 2:
       exitNicely("Not enough arguments given.")
    stream=args[-1]


    if stream == 'all':
        stream_loop = streams
    else:
        stream_loop = [stream]


    keywords = {}
    
    test = 0
    for stream_to_rerun in streams:
        print(stream_to_rerun)
        #import pdb;pdb.set_trace()
        
        file_path = os.path.join(base_path, stream_to_rerun + '_reextract_list.txt')
        command_to_run = cmd_line_finder(file_path, test)

        if command_to_run:

            command_parts = command_to_run.strip().split(' ')

            keywords = {'start': command_parts[3],
                        'end': command_parts[5],
                        'target_dir': command_parts[-2],
                        'qos' : command_parts[7]
                        }
            '''
            if stream_to_rerun == 'era5-m-nc':
                keywords['qos'] = 'large'

            if stream_to_rerun == 'era5-s-en-nc':
                keywords['qos'] = 'large'
            '''    
            dataset = command_parts[-1]

            with open(os.path.join(base_path,backlog_job_file),'a') as job_log_file:
                job_log_file.write(command_to_run)
                x = submit_job_rsync_netcdf_era5_new.MarsJob(dataset, keywords)   


        else:
            print('no more jobs')
