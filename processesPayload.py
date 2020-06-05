#%%
import requests
import pandas as pd
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pandas.io.json import json_normalize

# Set ipython's max row display
pd.set_option('display.max_row', 1000)

# Set iPython's max column width to 50
pd.set_option('display.max_columns', 50)

bld = pd.read_csv('dpw_buildings.csv',sep=';',dtype='str')
bld.columns = map(str.lower, bld.columns)
listData = []
PARAMS = {'processState':'COMPLETED','LIMIT':'0'}
response = requests.get('https://integration227992-pmmopc.integration.ocp.'
                        'oraclecloud.com:443/ic/api/process/v1/'
                        'tasks?'
                        'assignment=ALL','limit=5000',
                        auth=('flip@profmap.com', '!Flip1944!'))

data = response.json()
items = data['items']
headers = {'Accept': 'application/json'}
df = json_normalize(items)
new = df.title.str.split(",", n = 1, expand = True)
df['building_id'] = new[0]
df = df[df.processId != 251554]
dfm = pd.merge(df,bld,how='outer',on = 'building_id')
dfm.to_csv('tasks.csv',sep=';')

#%%
dfp=pd.DataFrame()

cnt=0
for index, row in dfm.iterrows():
    try:
        number = int(row.number)
        responsetask = requests.get('https://integration227992-pmmopc.'
                                'integration.ocp.oraclecloud.com:'
                                '443/bpm/api/4.0/tasks/' + str(number) + '/payload'
                                ,auth=('flip@profmap.com', '!Flip1944!'), headers=headers)


        taskdata = responsetask.json()
        dft = json_normalize(taskdata)
        dft['taskNumber'] = int(number)
        dfp = dfp.append(dft, sort=False)


    except:
        print('Error.....')
        #print(processId)
        print(number)
    print(number)
    cnt+=1
    print(cnt)

dfm.to_csv('c:/Users/flip/Documents/NDPW/tasks.csv',sep=';')
dfp.to_csv('c:/Users/flip/Documents/NDPW/tasksPayload.csv',sep=';')
tdf = dfm.merge(dfp,how='outer',left_on='number',right_on='taskNumber')
#%%
print('Getting Processes.....')
response = requests.get('https://integration227992-pmmopc.integration.ocp.oraclecloud.com:443/ic/api/process/v1/processes?processState=OPEN'
                        '&processName=Verification&assignmentFilter=ALL&limit=5000&processState=COMPLETED&processState=SUSPENDED',
                        auth=('flip@profmap.com', '!Flip1944!'))

data = response.json()
items = data['items']
headers = {'Accept': 'application/json'}
dp= json_normalize(items)
dp.to_csv('c:/Users/flip/Documents/NDPW/processes.csv',sep=';')
dfall = tdf.merge(dp,how='outer',left_on='processId_x',right_on='processId')
dfall.to_csv('c:/Users/flip/Documents/NDPW/AllData.csv',sep=';')

print(cnt)
