#%%
print("Hello")
from reportlab.pdfgen import canvas

def hello(c):
    c.drawString(100,100,"Hello World")

c = canvas.Canvas("hello.pdf")
hello(c)
c.showPage()
c.save()
print("Complete")

#%%
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

canvas = canvas.Canvas('myfile.pdf', pagesize=A4)
width, height = A4


#%%
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

file = open('tasks0612.csv','w')
PARAMS = {'assignment':'ALL'}
dpw = 'https://db.profmapcloud.com/ords/PDB1/dpw/buildings/'
response = requests.get('https://integration227992-pmmopc.integration.ocp.oraclecloud.com:443/bpm/api/4.0/tasks?limit=0',
                        auth=('flip@profmap.com', '!Flip1944!'),params=PARAMS)
data = response.json()
cnt=0
items = data['items']
headers = {'Accept': 'application/json'}
for i in items:
    response_task = requests.get('https://integration227992-pmmopc.integration.ocp.oraclecloud.com:443/bpm/api/4.0/tasks/'+str(i['number']),
                                auth=('flip@profmap.com', '!Flip1944!'))
    data_task = response_task.json()
    ass = data_task['assignees']['items']
    for a in ass:
        swimlane = a['id']
    title = i['title'].split('/')
    file.write('{0};{1};{2}\n'.format(title[0],swimlane,i['number']))
    print('Title = {0} : Swimlane = {1};{2}'.format(title[0],swimlane,i['number']))
    urlstr='https://integration227992-pmmopc.integration.ocp.oraclecloud.com:443/bpm/api/4.0/tasks/'+str(i['number'])+'/payload'
    response_payload = requests.get(urlstr,auth=('flip@profmap.com', '!Flip1944!'),headers=headers)
    data_payload = response_payload.json()
    filep = open(str(i['number'])+'_0612.json', 'w')
    filep.write(str(data_payload))
    filep.close()
    #bldresponse = requests.get(dpw + building_id, verify=False)
    #blddata = bldresponse.json()
    #region = blddata['region']
    #priority = blddata['priority']
    #print(building_id,swimlane)
    cnt+=1


file.close()
print(cnt)

#%%
import ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
cafile = 'cacert.pem'
bld = 'https://db.profmapcloud.com/ords/PDB1/dpw/buildings/2013'
bldresponse = requests.get(bld,verify=False)
blddata = bldresponse.json()
