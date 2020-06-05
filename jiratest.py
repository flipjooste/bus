# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import json
import smtplib


startAt = '0'
maxResults = '100'
url = "https://profmap.atlassian.net/rest/api/3/search"
auth = HTTPBasicAuth("sam@profmap.com", "pwcA9qBrCxKutphVhqzo2D4D")
headers = {
   "Accept": "application/json"
}
query = {
   'jql': 'project = NDPW and status = done' ,
    "startAt": startAt,
    "maxResults": maxResults
}
response = requests.request(
   "GET",
   url,
   headers=headers,
   params=query,
   auth=auth,
)
data = response.json()
totalLoop = int(int(data['total'])/100 + 1)

resultsDone = []
i=0
while i < totalLoop:
    print(i)
    query = {
        'jql': 'project = NDPW and status = done',
        "startAt": str(i*100),
        "maxResults": maxResults
    }
    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query,
        auth=auth,
    )
    data = response.json()
    issues = data['issues']
    for iss in issues:
        pmmId = int(iss['fields']['customfield_10031'])
        region = iss['fields']['customfield_10029']
        summary = iss['fields']['summary']
        key = iss['key']
        assignee = iss['fields']['assignee']
        if assignee:
            assignee = iss['fields']['assignee']['displayName']
        s = iss['fields']['statuscategorychangedate']
        statuscategorychangedate = s[:19].replace('T', ' ')
        resultsDone.append([pmmId,region,key,statuscategorychangedate,assignee,summary])
        print(pmmId)
        print(key)
    i+=1

df = pd.DataFrame(resultsDone, columns=['pmmId','region','key',
                                        'statuscategorychangedate','assignee','summary'])
df.to_csv('jiraTodo.csv',sep=';')
dfp = pd.read_csv('processes.csv',sep=';',usecols=['pmmid'])
dfm=pd.merge(df,dfp,how='left',left_on=df.pmmId,right_on=dfp.pmmid)
dfm = dfm.drop('key_0', 1)
dfm.to_csv('jira_add_to_opc.csv',sep=';')
dfm1=pd.merge(dfp,df,how='left',left_on=dfp.pmmid,right_on=df.pmmId)
dfm1 = dfm1.drop('key_0', 1)
dfm1.to_csv('opc_add_to_jira.csv',sep=';')
s = dfm[dfm['pmmid'].isnull()]
toOpc = s.pmmid
s = dfm1[dfm1['pmmId'].isnull()]
toJira = s.pmmid

PORT = 587
HOST = "email-smtp.us-east-1.amazonaws.com"
USERNAME = 'AKIAWGNBHIFYE424IOYY'
PASSWORD = 'BNHd5Ydzc1K+oY/1V2apCumGnXhzuiXQ+sN4TTNRspZ7'
server = smtplib.SMTP(HOST, PORT)
server.starttls()
server.login(USERNAME, PASSWORD)
msg = 'From:flip@profmap.com\nTo:jooste.flip@gmail.com\n' \
      'Subject:Add From Jira to OPC\n\n'+toOpc.to_string()
msg1 = 'From:flip@profmap.com\nTo:jooste.flip@gmail.com,flip@profmap.com\n' \
      'Subject:Add From OPC to Jira\n\n'+toJira.to_string()
server.sendmail('flip@profmap.com','jooste.flip@gmail.com,flip@profmap.com',msg)
server.sendmail('flip@profmap.com','jooste.flip@gmail.com',msg1)
