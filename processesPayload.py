#%%
import requests
import pandas as pd
import json
from timeit import default_timer as timer
from datetime import timedelta
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pandas.io.json import json_normalize

# Set ipython's max row display
pd.set_option('display.max_row', 1000)

# Set iPython's max column width to 50
pd.set_option('display.max_columns', 50)

bld = pd.read_csv('g:/dpw/dpw_buildings.csv',sep=';',dtype='str')
bld.columns = map(str.lower, bld.columns)
start = timer()
print('Getting Processes.....')
response = requests.get('https://integration227992-pmmopc.integration.ocp.oraclecloud.com:443/ic/api/process/v1/processes?processState=OPEN'
                        '&processName=Verification&assignmentFilter=ALL&limit=15000&processState=COMPLETED&processState=SUSPENDED',
                        auth=('flip@profmap.com', '!Flip1944!'))

data = response.json()
items = data['items']
headers = {'Accept': 'application/json'}
dp= json_normalize(items)
dp.to_csv('g:/dpw/processes.csv',sep=';')
end = timer()
print(timedelta(seconds=end-start))
#%%
#listData = []
print('Getting Tasks.....')

PARAMS = {'processState':'COMPLETED','LIMIT':'0'}
headers = {'Accept': 'application/json'}

dft=pd.DataFrame()
offset=0
while True:
    start = timer()
    response = requests.get('https://integration227992-pmmopc.integration.ocp.oraclecloud.com'
                        '/ic/api/process/v1/tasks?assignment=ALL&limit=500&process=Verification&offset='+str(offset),
                        auth=('flip@profmap.com', '!Flip1944!'))

    data = response.json()
    items = data['items']
    df = json_normalize(items)
    dft = dft.append(df, sort=False)
    offset=offset+500
    totalResults = data['totalResults']
    end = timer()
    print(timedelta(seconds=end - start))
    print('{0} of {1}'.format(offset,totalResults))
    if data['hasMore'] is False:
        break

dft['tmp'] = dft.title.str.replace(' ',',')
dft['tmp'] = dft.tmp.str.replace('FULFULL','')
new = dft.tmp.str.split(",", n = 1, expand = True)
dft['building_id'] = new[0]
dft=dft.drop(['tmp'],axis=1)
dft = dft[dft.processId != 251554]
dfm = pd.merge(dft,bld,how='outer',on = 'building_id')
dfm = dfm[dfm.processId != 251554]
dfm.to_csv('g:/dpw/tasks.csv',sep=';')

#%%
print('Getting Payload.....')
dfm = dfm[dfm.processId != '251554']
dfp=pd.DataFrame()
payload = {}

oracleUrl = 'https://sv1jzpkwobsfa0y-pmm.adb.eu-frankfurt-1.oraclecloudapps.com/ords/pmm/dpw/building/'

cnt=0
for index, row in dfm.iterrows():
  #if row.number == 214157:
    try:
      number = int(row.number)
      if number:
        processId = int(row.processId)
        responsetask = requests.get('https://integration227992-pmmopc.'
                                'integration.ocp.oraclecloud.com:'
                                '443/bpm/api/4.0/tasks/' + str(number) + '/payload'
                                ,auth=('flip@profmap.com', '!Flip1944!'), headers=headers)


        taskdata = responsetask.json()
        dft = json_normalize(taskdata)
        dft['taskNumber'] = int(number)
        dft['processId'] = int(processId)
        dft['processDefId'] = row.processDefId
        dft['building_id'] = row.building_id
        dft['fromUserDisplayName'] = row.fromUserName
        dft['assignees'] = row['assignees.items'][0].get('id').replace('Public Works.','')
        dft['priority'] = row.priority_y
        dft['local_mun'] = row.local_mun
        dft['district_mun'] = row.district_mun
        dft['town_name'] = row.town_name
        dft['createdDate'] = row.createdDate
        dft['updatedDate'] = row.updatedDate
        dft.createdDate = dft.createdDate.str.replace('T', ' ')
        dft.createdDate = dft.createdDate.str.replace('.000Z', '')
        dft.updatedDate = dft.updatedDate.str.replace('T', ' ')
        dft.updatedDate = dft.updatedDate.str.replace('.000Z', '')
        dfp = dfp.append(dft, sort=False)
        building_id = int(row.building_id)
        payload["facility_name"] = taskdata["inputTextFacilityName"]
        payload["facility_type"] = taskdata["selectFacility"]
        payload["function_of_structure"] = taskdata["selectFuncStruct"]
        payload["land_user"] = taskdata["selectUser"]
        try:
            payload["number_of_floors"] = taskdata["numberFloors"]
        except:
            payload["number_of_floors"] = '0'
        payload["address"] = taskdata["textAreaAddress"]
        payload["comments"] = taskdata["textAreaComments"]
        payload["to_device"] = "N"
        payload["checklistqa"] = '~'.join(taskdata["checklistQA"])
        payload["p_id"] = int(processId)
        payload["PlusCode"] = taskdata["inputTextPlusCode"]
        payload["googlemap"] = taskdata["link"]
        payload["s3link"] = taskdata["linkFiles"]
        payload["createddate"] = dft.createdDate.to_list()[0]
        payload["updateddate"] = dft.updatedDate.to_list()[0]
        payload["task_id"] = int(row.number)
        payload["creator"] = dft.fromUserDisplayName.to_list()[0]
        payload["reviewer"] = dft.assignees.to_list()[0]

        print('Update Building : {0} with processId : {1}'.format(building_id,processId))
        r = requests.put(oracleUrl + str(building_id), json=payload, headers=headers)
        dft['restcode'] = r.status_code
        #print(payload)
        print('POST /tasks/ {}'.format(r.status_code))
        if r.status_code != 200:
            print('Rest Error')
            break

    except:
        print('Error with Building .....')
        #print(processId)
        print(building_id)
        break
    cnt+=1
    print(cnt)
    #break
    #if cnt > 10:
    #    break

 #%%
dfp.to_csv('g:/dpw/tasksPayload.csv',sep=';')
#dfp = pd.read_csv('g:/dpw/tasksPayload.csv',sep=';')
tdf = dfm.merge(dfp,how='outer',left_on='number',right_on='taskNumber')
dfall = tdf.merge(dp,how='outer',left_on='processId_x',right_on='processId')
dfall.to_csv('g:/DPW/AllData.csv',sep=';')
print(cnt)
print('Completed.....')

