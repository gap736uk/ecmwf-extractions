"""
sl_tmp.py
===========

Template for the SLURM header for a job.
replacement for ll_tmp.py

"""

sl_commands=['#!/bin/bash',
             '#SBATCH --qos=normal',
             '#SBATCH --workdir=/scratch/ms/gb/ukc/scratchdir/',
             '#SBATCH --mail-type=FAIL',
	         '#SBATCH --output=/home/ms/gb/ukc/slurm_output/%N.%j.out',
	         '#SBATCH --error=/home/ms/gb/ukc/slurm_output/%N.%j.out',
             'export RSYNC_CONNECT_PROG="/usr/bin/connect -H proxy.ecmwf.int:2222 %H 873" ',
             'export MARS_MULTITARGET_STRICT_FORMAT=1']       

sl_commands_long=['#!/bin/bash',
             '#SBATCH --qos=long',
             '#SBATCH --workdir=/scratch/ms/gb/ukc/scratchdir/',
             '#SBATCH --mail-type=FAIL',
	         '#SBATCH --output=/home/ms/gb/ukc/slurm_output/%N.%j.out',
	         '#SBATCH --error=/home/ms/gb/ukc/slurm_output/%N.%j.out',
             'export RSYNC_CONNECT_PROG="/usr/bin/connect -H proxy.ecmwf.int:2222 %H 873" ',
             'export MARS_MULTITARGET_STRICT_FORMAT=1']
             

sl_commands_large=['#!/bin/bash',
	         '#SBATCH --qos=large',
             '#SBATCH --workdir=/scratch/ms/gb/ukc/scratchdir/',
             '#SBATCH --mail-type=FAIL',
	         '#SBATCH --output=/home/ms/gb/ukc/slurm_output/%N.%j.out',
	         '#SBATCH --error=/home/ms/gb/ukc/slurm_output/%N.%j.out',
             'export RSYNC_CONNECT_PROG="/usr/bin/connect -H proxy.ecmwf.int:2222 %H 873" ',
             'export MARS_MULTITARGET_STRICT_FORMAT=1']
             
sl_commands_express=['#!/bin/bash',
	         '#SBATCH --qos=express',
             '#SBATCH --workdir=/scratch/ms/gb/ukc/scratchdir/',
             '#SBATCH --mail-type=FAIL',
	         '#SBATCH --output=/home/ms/gb/ukc/slurm_output/%N.%j.out',
	         '#SBATCH --error=/home/ms/gb/ukc/slurm_output/%N.%j.out',
             'export RSYNC_CONNECT_PROG="/usr/bin/connect -H proxy.ecmwf.int:2222 %H 873" ',
             'export MARS_MULTITARGET_STRICT_FORMAT=1']
