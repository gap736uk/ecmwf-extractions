#!/usr/bin/python3.6

import os
import subprocess
import sys
import time

stream_templates = {'era5-s-en-nc':'.mem[number].[shortName].grb',
                    'era5-s-en-nc-1':'.mem[number].[shortName].grb',
                    'era5-s-en-nc-2':'.mem[number].[shortName].grb',
                    'era5-s-en-nc-3':'.mem[number].[shortName].grb',
                    'era5-m-nc': '.[shortName].grb',
                    'era5-s-en-sd-nc': '.[shortName].grb',
                    'era5-s-en-mean-nc': '.[shortName].grb',
                    'era5-s-nc': '.[shortName].grb',
                    'era5-s-fc-nc': '[step].[shortName].grb',
                    }


EXPECTED_MIN_SIZE = {'era5-s-en-nc': 196168800,
                     'era5-s-en-nc-1': 196168800,
                     'era5-s-en-nc-2': 196168800,
                     'era5-s-en-nc-3': 196168800,
                     'era5-m-nc': 1712107200,
                     'era5-s-en-sd-nc': 19616880,
                     'era5-s-en-mean-nc': 19616880 ,
                     'era5-s-nc': 26886360,
                     'era5-s-fc-nc': 199353600,                    
                    }

def submit_list(grib_file_list, stream):

    
    if 'era5t' in stream:
        dest_folder = '/scratch/ukc/era5t_extract/%s'% stream
        era5_stream = stream.replace('era5t-','era5-')
        expected_size = EXPECTED_MIN_SIZE[era5_stream]
        
    elif 'era51' in stream:
        dest_folder = '/scratch/ukc/era51_extract/%s'% stream
            
    else:
        dest_folder = '/scratch/ukc/era5_extract/%s'% stream
        expected_size = EXPECTED_MIN_SIZE[stream] 
        
    
    
    if 'era5t-' in stream:
        stream = stream.replace('era5t-','era5-')
    
    for grib_file in grib_file_list:
        grib_file = grib_file.strip()
        
        
        stats = os.stat(grib_file)
        last_mod_time = stats.st_mtime
        size = stats.st_size
        
        if time.time() - last_mod_time > 120 and size >= expected_size:
            name_bit = os.path.basename(grib_file)
            split_file_template = os.path.join(dest_folder, name_bit)
            output_template = split_file_template.replace('.grb',stream_templates[stream])
            pro = subprocess.call(['grib_copy', grib_file,  output_template])        

            if os.path.exists(grib_file):
                os.remove(grib_file)

if __name__== "__main__":
     
    args = sys.argv
    temp_file = args[1]
    stream = args[2]
    
     
    if os.path.exists(temp_file):
        
        with file(temp_file,'r') as grib_list_file:
        
            grib_file_list = grib_list_file.readlines()
     
            submit_list(grib_file_list, stream)
    
    os.remove(temp_file)
    
