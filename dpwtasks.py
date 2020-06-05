#%%
import requests
import time
import pandas as pd

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#file = open('dpwtasks.csv','w')
#file.write('processid;state;user;tasktype;taskid;action;pmmid;region;priority;updatedDate;updatedByDisplayName\n')
PARAMS = {'processState':'OPEN','LIMIT':'0'}
dpw = 'https://db.profmapcloud.com/ords/PDB1/dpw/buildings/'
response = requests.get('https://integration227992-pmmopc.integration.ocp.'
                        'oraclecloud.com:443/bpm/api/4.0/processes?processState=OPEN&processState=COMPLETED&limit=5000',
                        auth=('flip@profmap.com', '!Flip1944!'))
data = response.json()
cnt=0
items = data['items']
headers = {'Accept': 'application/json'}

processData = []
cnt=0
for i in items:  #Loop all processes
    processId = i['processId']
    processState = i['state']
    print('New ProcessID {0} , State {1}'.format(processId,processState))
    response_process = requests.get('https://integration227992-pmmopc.integration.ocp.oraclecloud.com:443/bpm/api/4.0/processes/'+str(i['processId']+'/audit?graphicFlag=False'),
                                auth=('flip@profmap.com', '!Flip1944!'))
    data_process = response_process.json()
    history = data_process['processHistory']
    for h in history:
        addFlag=0
        activityId = h['activityId']
        activityType = h['activityType']
        state = h['state']['description']
        activityName = h['activityName']
        tempstr = h['updatedDate'].split('T')
        activityDate = tempstr[0]
        activityTime = tempstr[1][0:-5]
        if activityType == 'START_EVENT' and state == 'Activity completed':
            updatedByDisplayName = 'START'
            userTaskNumber = '0'
            userTaskTitle='START'
            addFlag=1
        else:
            if activityType == 'USER_TASK' and state == 'Activity completed':
                #updatedByDisplayName = h['updatedByDisplayName']
                userTaskNumber = h['userTaskNumber']
                userTaskTitle = h['userTaskTitle']
                addFlag=1
        if addFlag == 1:
            print(state)
            print(activityId)
            print(activityName)
            print(activityType)
            print(activityDate)
            print(activityTime)
            #print(updatedByDisplayName)
            print(userTaskNumber)
            print(userTaskTitle)
            print('-----------')
            #processData.append([processId,processState,activityId,activityType,state,activityName,activityDate,
            #                    activityTime,updatedByDisplayName,userTaskNumber,userTaskTitle])
            processData.append([processId,processState,activityId,activityType,state,activityName,activityDate,
                                activityTime,userTaskNumber,userTaskTitle])


    #cnt+=1
    #print(cnt)
    #if cnt > 20:
    #    break

df = pd.DataFrame(processData, columns=['processId','processState','activityId',
                                        'activityType','state','activityName','activityDate',
                                        'activityTime','updatedByDisplayName','userTaskNumber','userTaskTitle'])

df.to_csv('dpwtasks.csv',sep=';')
#print(cnt)
