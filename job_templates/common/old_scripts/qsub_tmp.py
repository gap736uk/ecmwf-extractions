"""
qsub_tmp.py
===========

Template for the qsub header for a job.

"""

qsub_commands=['# QSUB -r JOB_NAME_HERE', 
               '# QSUB -lT 40000',
               '# QSUB -lM 5mw',
               '# QSUB -q mars',
               '# QSUB -s /bin/ksh',
               '# QSUB -eo',
               '# QSUB']
