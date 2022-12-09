"""
slconvert_to_netcdf.py
===============

Template file for conversion to netCDF section of job

"""
convert_commands="""#
#
# This section creates a loop around the convert 
# command so that if the number of files in this
# directory is longer than the glob limit it will
# move them out 1000 at a time and convert to another netCDF 
# another directory
#

# Initialise file list and length of it
file_list=`ls`
num_of_files=`ls *.grb| wc -w`

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
  # mkdir convert_1000
  # mv $next_1000_files convert_1000
  # cd convert_1000
  
  for f in $next_1000_files
  do
      echo $f
      
      name_bit=` basename $f .grb`
      grib_to_netcdf $f -o $name_bit.nc -k 4 -d 1 -s
      rm $f
done
"""

convert_commands_new="""#
#
# This section creates a loop around the convert 
# command so that if the number of files in this
# directory is longer than the glob limit it will
# move them out 1000 at a time and convert to another netCDF 
# another directory
#

# Initialise file list and length of it
file_list=`ls`
num_of_files=`ls *.grb| wc -w`

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
  # mkdir convert_1000
  # mv $next_1000_files convert_1000
  # cd convert_1000
  
  for f in $next_1000_files
  do
      echo $f
      
      name_bit=` basename $f .grb`
      grib_to_netcdf $f -o $name_bit.nc -k 4 -d 1 -s
      rm $f
done
"""
