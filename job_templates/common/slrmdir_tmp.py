"""
rmdir_tmp.py
============

Template file for the remove directories section of a job.

"""

rmdir_commands=['if [ `pwd` = /home/ms/gb/ukc ]','  then',
                '    echo "Stopped from deleting in HOME directory so exiting!"',
                '    exit',
		'fi',
                'rm *',
                'cd $HOME',
                ]

