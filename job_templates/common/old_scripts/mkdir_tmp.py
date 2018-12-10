"""
mkdir_tmp.py
============

Template for the make directory section of a job.

"""

mkdir_commands=['WORK=$SCRATCH/JOB_NAME_HERE$$',
                'mkdir -p $WORK',
                'if [ $? != 0 ]','  then', 
                '  echo "Could not make scratch directory so exiting!"', 
                '  exit', 'fi', 
                'cd $WORK']
