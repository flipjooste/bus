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

#%%
from reportlab.pdfgen import canvas
 def hello(c):
 c.drawString(100,100,"Hello Flip World")
 c = canvas.Canvas("helloflip.pdf")
 hello(c)
 c.showPage()
 c.save()

#%%

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

canvas = canvas.Canvas("form.pdf", pagesize=letter)
canvas.setLineWidth(.3)
canvas.setFont('Helvetica', 12)

canvas.drawString(30, 750, 'OFFICIAL COMMUNIQUE')
canvas.drawString(30, 735, 'OF ACME INDUSTRIES')
canvas.drawString(500, 750, "12/12/2010")
canvas.line(480, 747, 580, 747)

canvas.drawString(275, 725, 'AMOUNT OWED:')
canvas.drawString(500, 725, "$1,000.00")
canvas.line(378, 723, 580, 723)

canvas.drawString(30, 703, 'RECEIVED BY:')
canvas.line(120, 700, 580, 700)
canvas.drawString(120, 703, "JOHN DOE")

canvas.save()