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
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

dpw = 'https://db.profmapcloud.com/ords/PDB1/dpw/buildings/'
response = requests.get('https://integration227992-pmmopc.integration.ocp.oraclecloud.com:443/bpm/api/4.0/processes?limit=0',
                        auth=('flip@profmap.com', '!Flip1944!'))
data = response.json()
cnt=0
items = data['items']
for i in items:
    processNumber = i['processNumber']
    response = requests.get('https://integration227992-pmmopc.integration.ocp.oraclecloud.com:443/bpm/api/4.0/task'+str(processNumber),
        auth=('flip@profmap.com', '!Flip1944!'))
    data = response.json()
    cnt = 0
    items = data['items']
    ass = i['assignees']['items']
    for a in ass:
        swimlane = a['id']
    #bldresponse = requests.get(dpw + building_id, verify=False)
    #blddata = bldresponse.json()
    #region = blddata['region']
    #priority = blddata['priority']
    print(building_id,swimlane)
    cnt+=1

print(cnt)

#%%
import ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
cafile = 'cacert.pem'
bld = 'https://db.profmapcloud.com/ords/PDB1/dpw/buildings/2013'
bldresponse = requests.get(bld,verify=False)
blddata = bldresponse.json()
