#%%
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

file = open('processes0412.csv','w')
file.write('processid;state;user;tasktype;taskid;action;pmmid;region;priority\n')
PARAMS = {'processState':'OPEN','LIMIT':'0'}
dpw = 'https://db.profmapcloud.com/ords/PDB1/dpw/buildings/'
response = requests.get('https://integration227992-pmmopc.integration.ocp.'
                        'oraclecloud.com:443/bpm/api/4.0/processes?processState=OPEN&limit=0',
                        auth=('flip@profmap.com', '!Flip1944!'))
data = response.json()
cnt=0
items = data['items']
headers = {'Accept': 'application/json'}
for i in items:  #Loop all processes
    processId = i['processId']
    processState = i['state']
    response_process = requests.get('https://integration227992-pmmopc.integration.ocp.oraclecloud.com:443/bpm/api/4.0/processes/'+str(i['processId']+'/audit?graphicFlag=False'),
                                auth=('flip@profmap.com', '!Flip1944!'))
    data_process = response_process.json()
    history = data_process['processHistory']
    for h in history:
        #tasknumber = 0
        #taskstate = ''
        activityName = h['activityName']
        activityType = h['activityType']
        if activityType == 'USER_TASK':
            taskHistory = h['taskHistory']
            for th in taskHistory:
                tasknumber = th['number']
                taskstate = th['state']
    urlstr = 'https://integration227992-pmmopc.integration.ocp.oraclecloud.com:443/bpm/api/4.0/tasks/' + str(
        tasknumber) + '/payload'
    response_payload = requests.get(urlstr, auth=('flip@profmap.com', '!Flip1944!'), headers=headers)
    data_payload = response_payload.json()

    try:
        pmmbld = data_payload['inputTextPmmBldId']
        bldresponse = requests.get(dpw + pmmbld, verify=False)
        blddata = bldresponse.json()
        region = blddata['region']
        priority = blddata['priority']
        print('{0};{1};{2};{3};{4};{5};{6};{7};{8}'.
            format(processId,processState,activityName,activityType,tasknumber, taskstate,pmmbld,region,priority))
        file.write('{0};{1};{2};{3};{4};{5};{6};{7};{8}\n'.
            format(processId,processState,activityName,activityType,tasknumber, taskstate,pmmbld,region,priority))
    except:
        print('Error : {0}'.format(processId))


    cnt+=1
    #if cnt > 10:
    #    break


file.close()
print(cnt)
