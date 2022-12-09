from datetime import datetime




#stream_targets = {'era5-s-nc': 'ecmwf-era5',
#                  'era5-s-fc-nc': 'ecmwf-era5-fc',
#                  'era5-m-nc': 'ecmwf-era5-model',
#                  'era5-s-en-nc': 'ecmwf-era5-en-mem',
#                  'era5-s-en-sd-nc': 'ecmwf-era5-en-mean',
#                  'era5-s-en-mean-nc': 'ecmwf-era5-en-mean',
#                  }


stream_targets = {'era51-s-nc': 'ecmwf-era51',
                  'era51-s-fc-nc': 'ecmwf-era51-fc',
                  'era51-m-nc': 'ecmwf-era51-model',
                  'era51-s-en-nc': 'ecmwf-era51-en-mem',
                  'era51-s-en-sd-nc': 'ecmwf-era51-en-mean',
                  'era51-s-en-mean-nc': 'ecmwf-era51-en-mean',
                  }


for stream,target in stream_targets.items():
    with open('%s'% stream,'w') as output_file :
        date_parts = {'startday': '01',
                  'target' : target, 
                  'stream': stream}


        for year in range(2007,1999, -1):
            date_parts['year'] = str(year)

            for month in range(12,0, -1):


                if month in [1,3,5,7,8,10,12]:
                    endday = 31
                else:
                    if month == 2:
                        if year%4:
                            endday = 28
                        else:
                            endday = 29
                    else:
                        endday = 30
                month = str(month)

                if month not in ['10','11','12']:
                    month = '0' + month

                date_parts['month'] = month
                date_parts['endday'] = endday

                output_file.write('$HOME/cronjobs/cronrun.bsh /home/ms/gb/ukc/submit_job_rsync_netcdf_era5_new.py -s %(year)s%(month)s%(startday)s -e %(year)s%(month)s%(endday)s --qos long -target %(target)s %(stream)s\n'% date_parts)
