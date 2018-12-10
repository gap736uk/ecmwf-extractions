"""
sl_tmp.py
===========

Template for the SLURM header for a job.
replacement for ll_tmp.py

"""

sl_commands=['#!/bin/bash',
             ' ',
             'SBATCH --qos=normal',
             'SBATCH --workdir=/scratch/ms/gb/ukc/scratchdir/',
             'SBATCH --mail-type=FAIL',
             'SBATCH --output=/home/ms/gb/ukc/slurm_output/slurm-%j.out',
             'SBATCH --error=/home/ms/gb/ukc/slurm_output/slurm-%j.err']		       
