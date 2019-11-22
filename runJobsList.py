
import os

range = '-start 20100503 -end 20100508'
jobsList = ['submit_job.py %s -target /deliveries/ecmwf-op/op-n80/ ~/job_templates/op/op-1.0-fs'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-1.125/ ~/job_templates/op/op-1.125-am'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-1.125/ ~/job_templates/op/op-1.125-ap'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-1.125/ ~/job_templates/op/op-1.125-as'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-1.125/ ~/job_templates/op/op-1.125-at'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-1.125/ ~/job_templates/op/op-1.125-fm'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-1.125/ ~/job_templates/op/op-1.125-fs'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-2.5/ ~/job_templates/op/op-2.5-ap'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-2.5/ ~/job_templates/op/op-2.5-as'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-2.5-mm/ ~/job_templates/op/op-2.5-mm'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-n80/ ~/job_templates/op/op-n80-as'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-n80r/ ~/job_templates/op/op-n80r-am'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-n80r/ ~/job_templates/op/op-n80r-ap'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-n80r/ ~/job_templates/op/op-n80r-as'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-n80r/ ~/job_templates/op/op-n80r-at'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-n80r/ ~/job_templates/op/op-n80r-av'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-n80r/ ~/job_templates/op/op-n80r-fm'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-n80r/ ~/job_templates/op/op-n80r-fs-moda'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-n80r/ ~/job_templates/op/op-n80r-fs'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-n80r/ ~/job_templates/op/op-n80r-fs_named_by_step'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-t159/ ~/job_templates/op/op-t159-am'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-t159/ ~/job_templates/op/op-t159-ap'
, 'submit_job.py %s -target /deliveries/ecmwf-op/op-t159/ ~/job_templates/op/op-t159-at'
]

for job in jobsList:
   jobSubmit = job% range
   os.system(jobSubmit)
   os.system('sleep 3')