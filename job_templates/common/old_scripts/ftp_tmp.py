"""
ftp_tmp.py
==========

Template file for FTP section of job

"""

ftp_commands="""#
# This section creates a loop around the FTP
# command so that if the number of files in this
# directory is longer than the glob limit it will
# move them out 1000 at a time and FTP them from 
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
  if [ $len -lt $num ]   # If less than glob limit FTP all
    then
    next_1000_files=$file_list
    file_list=""
  else                   # otherwise get first 1000 files
    next_1000_files=` echo $file_list | cut -d\" \" -f1-$num `
    file_list=` echo $file_list | cut -d\" \" -f$num- `
  fi
  num_of_files=` echo $file_list | wc -w ` 
  
  # Now move the files to a temporary dir
  # and FTP across
  mkdir ftp_1000
  mv $next_1000_files ftp_1000
  cd ftp_1000
    
  # Now do the FTPing
  ftp -n ftp-gw.ecmwf.int <<EOF
    user badc\@tornado.badc.rl.ac.uk rain&h@il
    cd DELIVERIES_DIR
    cd TARGET_DIR  
    umask 037
    bin
    mput *
    quit
EOF
  
  # Now delete those files that have been FTPed
  cd ..
  rm -fR ftp_1000
  
done
"""
