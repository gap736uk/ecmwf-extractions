#!/usr/bin/python3.6


import subprocess
import calendar
import datetime
import os
import sys
import submit_job_rsync_netcdf
from elasticsearch import Elasticsearch
import requests


query = {
	"query": {"match_all": {}}
}


'''
es.search(index="ceda-fbi", body=query)
es.indices.get_mapping(index="ceda-fbi")
'''



es_url = 'https://jasmin-es1.ceda.ac.uk/ceda-fbi/_search'

def poll_fbi(dir_path):

    query = {
                "query": {
                    "match_phrase_prefix": {
                        "info.directory.analyzed":dir_path
                    }
                },
                "size": 40
            }

    resp = requests.post(es_url, json=query)
    return resp


starting_dir = '/badc/ecmwf-era5/data/'

next_dir_map = {'era5-s-nc': 'oper/an_sfc',
                'era5-m-nc': 'oper/an_ml',
                'era5-s-fc-nc': 'oper/fc_sfc',
                'era5-s-en-nc': 'enda/an_sfc',
                'era5-s-en-mean': 'enda/em_sfc',
                'era5-s-en-sd' : 'enda/es_sfc'
                } 
                
target_dir_mapping = {'era5-s-nc': 'ecmwf-era5',
                'era5-m-nc': 'ecmwf-era5-model',
                'era5-s-fc-nc': 'ecmwf-era5-fc',
                'era5-s-en-nc': 'ecmwf-era5-en-mem',
                'era5-s-en-mean': 'ecmwf-era5-en-mean',
                'era5-s-en-sd' : 'ecmwf-era5-en-mean'
                }
                
def check_dir(selected_stream, year):

    year_dir = os.path.join(starting_dir, next_dir_map[selected_stream],year)


    for month_check in range(1,13):
        no_of_days = calendar.monthrange(int(year),month_check)[1]

        if month_check < 10:
            month_check = '0' + str(month_check)
        else:
            month_check = str(month_check)
        missing_days = []
        
        for day_of_month in range(1,no_of_days+1):
            if day_of_month < 10:
                day_of_month = '0' + str(day_of_month)
            else:
                day_of_month = str(day_of_month)
            
            date_to_check = os.path.join(year_dir,month_check, day_of_month)
            resp = poll_fbi(date_to_check)
            
            if not resp.json()['hits']['hits']:
                
                missing_days.append('%s%s%s'% (year,month_check,day_of_month))            
        if missing_days:
            return missing_days

if __name__ == "__main__":
    stream = sys.argv[1]
    for year in range(2019, 1979,-1):
    
        missing_days = check_dir(stream, str(year))

        if missing_days:
            missing_days[0], missing_days[-1]



            keywords = {'start': missing_days[0],
                            'end': missing_days[-1],
                            'target_dir': target_dir_mapping[stream],
                            'qos' : 'normal'
                            }
            if stream == 'era5-m-nc':
                keywords['qos'] = 'long'

            if stream == 'era5-s-en-nc':
                keywords['qos'] = 'large'

            print(keywords, stream)
            backfill_file = 'era5_control/%s-backfill.txt'%stream
            f = open(backfill_file, 'r')
            extracting_month = missing_days[0][0:6]
            
            lines = f.read()
            answer = lines.find('string')
            
            if not answer:
            
                with open(backfill_file,'w') as backfill_log:
                    backfill_log.write('%s|%s|%s'% (datetime.datetime.now().strftime('%Y%m%d'), keywords['start'], keywords['end']))
                    #x = submit_job_rsync_netcdf.MarsJob(stream, keywords) 
                break
