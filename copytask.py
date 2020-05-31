#%%
import requests
import pandas as pd
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pandas.io.json import json_normalize


headers = {'Accept': 'application/json'}
#%%
while(1):
    fromTask = input('From Task : ')
    toTask = input('To Task : ')
    responsetask = requests.get('https://integration227992-pmmopc.'
                                'integration.ocp.oraclecloud.com:'
                                '443/bpm/api/4.0/tasks/' + str(fromTask) + '/payload'
                                ,auth=('flip@profmap.com', '!Flip1944!'), headers=headers)

    taskdata = responsetask.json()
    r = requests.post('https://integration227992-pmmopc.'
                                'integration.ocp.oraclecloud.com:'
                                '443/bpm/api/4.0/tasks/' + str(toTask) + '/payload',
                                json = taskdata
                                ,auth=('flip@profmap.com', '!Flip1944!'), headers=headers)

    if r.status_code != 201:
        print('POST /tasks/ {}'.format(r.status_code))
