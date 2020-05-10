import requests
import pandas as pd
from pandas.io.json import json_normalize
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pandas.io.json import json_normalize

# Set ipython's max row display
pd.set_option('display.max_row', 1000)

# Set iPython's max column width to 50
pd.set_option('display.max_columns', 50)

print('Retreiving tasks.....')
bld = pd.read_csv('g:/dpw/dpw_buildings.csv',sep=';',dtype='str')
bld.columns = map(str.lower, bld.columns)
listData = []
PARAMS = {'processState':'COMPLETED','LIMIT':'0'}
response = requests.get('https://integration227992-pmmopc.integration.ocp.'
                        'oraclecloud.com:443/ic/api/process/v1/tasks?'
                        'assignment=ALL','limit=5000',
                        auth=('flip@profmap.com', '!Flip1944!'))

data = response.json()
items = data['items']
headers = {'Accept': 'application/json'}
df = json_normalize(items)
new = df.title.str.split(",", n = 1, expand = True)
df['building_id'] = new[0]
dfm = pd.merge(df,bld,how='inner',on = 'building_id')
dfm = dfm.drop(columns=['priority_x','ownerRole','status','state','hasSubTasksFlag','processName',
'processDefId','length','rel','href','processInstanceDetail.length','processInstanceDetail.rel',
'processInstanceDetail.href','assignees.hasMore'],axis=1)
dfm.to_csv('g:/dpw/tasks.csv',sep=';')
