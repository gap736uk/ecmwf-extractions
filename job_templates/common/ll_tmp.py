"""
ll_tmp.py
===========

Template for the LoadLeveler header for a job.

"""

ll_commands=['#!/bin/ksh',
             ' ',
	     '#@ class = normal',
	     '#@ cpu_limit = 1000',
	     '#@ output = ~/loadleveler_output/$(jobid)',
	     '#@ error =  ~/loadleveler_output/$(jobid)',
	     '#@ queue']		       
