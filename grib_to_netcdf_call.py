#!/usr/local/apps/python/2.7.12-01/bin/python

import os
import subprocess
import sys



def submit_list(grib_file_list, stream):

    
    if 'era5t' in stream:
        dest_folder = '/scratch/ms/gb/ukc/era5t_processed/%s'% stream
    elif 'era51' in stream:
        dest_folder = '/scratch/ms/gb/ukc/era51_processed/%s'% stream
    else:
        dest_folder = '/scratch/ms/gb/ukc/era5_processed/%s'% stream
    
    
    
    for grib_file in grib_file_list:
        grib_file = grib_file.strip()
        name_bit = os.path.basename(grib_file)[:-3] + 'nc'
        netcdf_file = os.path.join(dest_folder, name_bit)
        
        pro = subprocess.call(['grib_to_netcdf', grib_file,  '-o' , netcdf_file, '-k',  '4', '-d', '1'])
        
        if os.path.exists(netcdf_file):
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
    
