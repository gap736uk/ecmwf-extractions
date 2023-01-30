import ftplib


#!/usr/bin/python3.6

import os
import subprocess
import sys    
import fnmatch
from multiprocessing import Pool
import ftplib

FTP_PASSWORD = open('/home/ukc/ecmwf-extractions/job_templates/common/.ftppwd','r').readline().strip()

def upload(source_file_list, source_dir, target_dir):
    
    ftp = ftplib.FTP('arrivals.ceda.ac.uk')
    ftp.login("gparton",FTP_PASSWORD)
    ftp.cwd(f'{target_dir}')

    for fille in source_file_list:
        file_to_upload = os.path.join(source_dir,fille.strip())
        try:
        
            ftp.storbinary(f'STOR {fille.strip()}', open(file_to_upload,'rb'))
        except:
            pass
        else:
        
            os.remove(file_to_upload)

    ftp.quit()


if __name__== "__main__":
     
    args = sys.argv
     
    temp_file = args[1]
    source_dir = args[2]
    target_dir = args[3]
    
  
    if os.path.exists(temp_file):
        
        with open(temp_file,'r') as source_list_file:
        
            source_file_list = source_list_file.readlines()
     
            upload(source_file_list, source_dir, target_dir)
    
    os.remove(temp_file)
    
