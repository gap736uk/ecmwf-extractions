"""
sl_tmp.py
===========

Template for the SLURM header for a job.
replacement for ll_tmp.py

"""

sl_commands=['#!/bin/bash',
             '#SBATCH --chdir=/scratch/ukc/',
             '#SBATCH --mail-type=FAIL',
             '#SBATCH --output=/home/ukc/slurm_output/slurm-%j.out',
             '#SBATCH --error=/home/ukc/slurm_output/slurm-%j.err']                  

sl_commands_long=['#SBATCH --qos=el']
             
sl_commands_large=['#SBATCH --qos=el']
             
sl_commands_express=['#SBATCH --qos=ef']

sl_commands_timecrit1=['#SBATCH --qos=ef']		       

rsync_command =['export RSYNC_CONNECT_PROG="/usr/bin/connect -H proxy.ecmwf.int:2222 %H 873" ']

strict_command = ['export MARS_MULTITARGET_STRICT_FORMAT=1']
