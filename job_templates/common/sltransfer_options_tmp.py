"""
convert_tmp.py
===============

Template file for conversion to netCDF section of job

"""
transfer_commands="""#
#
# This section creates a loop around the convert 
# command so that if the number of files in this
# directory is longer than the glob limit it will
# move them out 1000 at a time and convert to another netCDF 
# another directory
#

# Initialise file list and length of it
file_list=`ls`
num_of_files=`ls | wc -w`

while [ $num_of_files -gt 0 ]
  do
  # Set maximum number of files to glob
  num=1000
  # Get current length of file list
  len=` echo $file_list | wc -w `
  if [ $len -lt $num ]   # If less than glob limit convert all
    then
    next_1000_files=$file_list
    file_list=""
  else                   # otherwise get first 1000 files
    next_1000_files=` echo $file_list | cut -d\" \" -f1-$num `
    file_list=` echo $file_list | cut -d\" \" -f$num- `
  fi
  num_of_files=` echo $file_list | wc -w ` 
  
  # Now move the files to a temporary dir
  # and rsync across
  mkdir rsync_1000
  mv $next_1000_files rsync_1000
  cd rsync_1000
    
  # Now do the scping
  #setenv RSYNC_CONNECT_PROG `/usr/bin/connect -H proxy.ecmwf.int:2222 %H 873`
  #$ENV{"RSYNC_CONNECT_PROG"} = `/usr/bin/connect -H proxy.ecmwf.int:2222 %H 873`

  rsync --password-file=/home/ms/gb/ukc/job_templates/common/.rsyncpwd ./* gparton@arrivals.ceda.ac.uk::gparton/TARGET_DIR --port=873 -v
  
  # Now delete those files that have been scped
  cd ..
  rm -fR rsync_1000
  
done
"""
