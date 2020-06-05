#%%
import requests
import pandas as pd
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pandas.io.json import json_normalize

listData = [
311161,
311165,
311170,
311177,
311180,
311187,
311189,
311191,
311194,
311196,
311199,
311201,
311206,
311210,
311212,
311214,
311217,
311228,
311318,
311323,
311333,
311349,
311353,
311370,
311378,
311380,
311415,
321122,
321124,
321126,
321129,
321131,
321133,
321145,
321149,
321152,
321154,
321159,
321161,
321216,
321238,
321244,
321246,
321248,
321270,
321323,
321325,
321327,
321329,
321333,
321335
]

#Public Works.ProcessReportCreator
#,'Public Works.DeptQA2'
#,'Public Works.DeptQA1'
#'Public Works.ProcessLS','Public Works.ProcessQA',
approvers = ['Public Works.DeptQA2']
taskdata = {"action":{"id":"APPROVE","type":"SYSTEM"}}
headers = {'Accept': 'application/json'}
flag = 1

while(flag == 1):
    print('Starting List ............\n')
    for i in listData:
        print(i)
        flag = 0
        response = requests.get('https://integration227992-pmmopc.integration.ocp.oraclecloud.com:443/bpm/api/4.0/'
                        'tasks?instanceId=' + str(i),
                         'assignment=ALL'
                        ,auth=('flip@profmap.com', '!Flip1944!'))

        data = response.json()
        #items = data['items']
        #data['flowChanges'][0]['sourceActivity']['locationInfo']['activityInfo']['displayName']
        role = data['items'][0]['assignees']['items'][0]['id']
        taskNumber = data['items'][0]['number']

        if role in approvers:
            print('Process: {0} , Task: {1} ,Reached: {2} '.format(i,taskNumber,role))
        else:
            print('Process: {0} , Task: {1} ,At Role {2}  .....'.format(i,taskNumber,role))
            r = requests.put('https://integration227992-pmmopc.integration.ocp.oraclecloud.com:443/bpm/api/4.0/'
                          'tasks/' + str(taskNumber),
                          json=taskdata
                          , auth=('flip@profmap.com', '!Flip1944!'), headers=headers)
            print(r)
            flag = 1

        #input('enter')



