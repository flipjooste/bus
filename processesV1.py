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

#%%
bld = pd.read_csv('dpw_buildings.csv',sep=';',dtype='str')
bld.columns = map(str.lower, bld.columns)
listData = []
PARAMS = {'processState':'COMPLETED','LIMIT':'0'}
response = requests.get('https://integration227992-pmmopc.integration.ocp.oraclecloud.com:443/ic/api/process/v1/processes?processState=OPEN'
                        '&processName=Verification&assignmentFilter=ALL&limit=5000&processState=COMPLETED&processState=SUSPENDED',
                        auth=('flip@profmap.com', '!Flip1944!'))

data = response.json()
items = data['items']
headers = {'Accept': 'application/json'}
df = json_normalize(items)
dfp=pd.DataFrame()
df.to_csv('c:/Users/flip/Documents/NDPW/processes.csv',sep=';')




#%%
cnt=0

for i in items:
    number = i['processId']
    response = requests.get('https://integration227992-pmmopc.'
                                'integration.ocp.oraclecloud.com:'
                                '443/ic/api/process/v1/processes/' + str(number) + '/dataobjects'
                                ,auth=('flip@profmap.com', '!Flip1944!'), headers=headers)

    data = response.json()
    try:
        dict = json.loads(data['dataVariableFlatTree'][0]['value'])
        print('Number : {0} : {1}'.format(number,dict))
        dft = pd.DataFrame([dict])
        dft['processId'] = number
        dfp = dfp.append(dft,sort=False)
        cnt+=1
        if cnt%10==0:
            print(cnt)
    except:
        print('Error....')
        print(number)


m = df.merge(dfp,how='outer',on = 'processId')
mblk = m.merge(bld,how='outer',left_on = 'inputTextPmmBldId',right_on='building_id')
mblk.to_csv('c:/Users/flip/Documents/NDPW/processDataObjects.csv',sep=';')