# coding: utf-8

# In[1]:

import boto3
import pandas as pd
from IPython.core.display import HTML

# In[2]:


import folium
from folium import plugins

#get_ipython().magic('matplotlib inline')

# In[1]:


import pandas as pd
import numpy as np
import time
import datetime
import cx_Oracle

# In[19]:


pd.set_option('display.height', 1000)
pd.set_option('max_columns', 1000)

# In[9]:


import boto3

i = 0
s3 = boto3.resource('s3')
df = pd.DataFrame(columns=["photoname"])

my_bucket = s3.Bucket('scholartransport')
for key in my_bucket.objects.filter(Prefix="faces/"):
    fname = key.key
    df = df.append({"photoname": fname}, ignore_index=True)
    i += 1
    if i % 10000 == 0:
        print(i)

# In[14]:


i = 0
df['route_guid'] = ''
df['lat'] = ''
df['lon'] = ''
df['gps_time'] = ''
df['user'] = ''
df['driver'] = ''
df['regnumber'] = ''
df['on_off'] = ''

# f = open('g:/gde/Bus/photosplit.csv','w')
for index, row in df.iterrows():
    fname = row['photoname']
    i += 1
    if i % 10000 == 0:
        print(i)
        # break
    if ((fname.find('_IN_') >= 0 or fname.find('_OUT_') >= 0) and fname.find('COMPLETED') < 0) and fname.find(
            '_-24') < 0:
        sname = fname.split('_')
        route_guid = sname[0][6:] + '_' + sname[1]
        if sname[3].startswith('-') or sname[3].startswith('0.0'):
            lat = sname[3]
            lon = sname[4]
            gps_time = sname[5] + ' ' + sname[6]
        elif sname[3].startswith('BUS'):
            lat = sname[7]
            lon = sname[8]
            gtemp = sname[9] + ' ' + sname[10]
            gps_time = gtemp.split('.')[0]
            user = sname[3]
            driver = sname[4]
            regnumber = sname[5]
        else:
            lat = sname[4]
            lon = sname[5]
            gps_time = sname[6] + ' ' + sname[7]
        on_off = sname[2]
        if on_off == 'IN':
            on_off = 'ON'
        else:
            on_off = 'OFF'
        df.at[index, 'route_guid'] = route_guid
        df.at[index, 'lat'] = lat
        df.at[index, 'lon'] = lon
        df.at[index, 'gps_time'] = gps_time
        df.at[index, 'user'] = user
        df.at[index, 'driver'] = driver
        df.at[index, 'regnumber'] = regnumber
        df.at[index, 'on_off'] = on_off
        # f.write('{0};{1};{2};{3};{4};{5};{6};{7}\n'.format(route_guid,lat,lon,gps_time,user,driver,regnumber,on_off))

# In[94]:
#s = pd.read_csv('c:/Users/flip/Documents/GDE/Bus/17 July Rekog routes stop Table.csv', dtype='str', encoding='ANSI',delimiter=';')
s = pd.read_csv('c:/Users/flip/Documents/GDE/Bus/sr_new.csv', dtype='str', encoding='ANSI',delimiter=',')
#%%
srn = pd.read_csv('c:/Users/flip/Documents/GDE/Bus/srn.csv', dtype='str', encoding='ANSI',delimiter=';')

# In[95]:
b = pd.read_csv('c:/Users/flip/Documents/GDE/Bus/bus_stops.csv', dtype='str')
#l = pd.read_csv('c:/Users/flip/Documents/GDE/Bus/17 july LEARNERS Table V1.csv',encoding='ansi' ,dtype='str',delimiter=';')
l = pd.read_csv('c:/Users/flip/Documents/GDE/Bus/learners.csv',encoding='ansi' ,dtype='str',delimiter=',')

# In[96]:
r = pd.read_csv('c:/Users/flip/Documents/GDE/Bus/routes.csv', dtype='str')

# In[99]:
s = s.fillna('na')
r = r.fillna('na')
b = b.fillna('na')
l = l.fillna('na')

# In[100]:
s.columns = map(str.lower, s.columns)
r.columns = map(str.lower, r.columns)
b.columns = map(str.lower, b.columns)
l.columns = map(str.lower, l.columns)
# In[101]:
s['gps_time'] = s.gps_time.str.split('.JPG', expand=True)[0]
s['gps_time'] = s.gps_time.str.replace('_', ' ')
s['gps_time'] = s.gps_time.str.replace('v', '')
s['capture_date'] = pd.to_datetime(s.gps_time)
#%%
s.sort_values(['routeguid_table','stopguid_table','stop_number'], inplace=True)

# In[110]:
#tmp = (b.stop_date == 'na') & (b.start_date != 'na')
#b['stop_date'] = b[tmp]['start_date']

#%%
b = b[b.start_date != 'na']
b = b[b.stop_date != 'na']
r = r[r.start_time!= 'na']

# In[111]:
r['capture_date'] = pd.to_datetime(r.route_date + ' ' + r.start_time)
b['stop_date'] = pd.to_datetime(b['stop_date'])
b['start_date'] = pd.to_datetime(b['start_date'])
b.sort_values('stop_date', inplace=True)
r.sort_values('capture_date', inplace=True)
new = b.start_gps.str.split(',', n=1, expand=True)
b['lat'] = pd.to_numeric(new[0])
b['lon'] = pd.to_numeric(new[1])

# In[92]:
s.index = s.capture_date
#%%
b.index = b.stop_date
r.index = r.capture_date

# In[8]:
b = pd.merge(b, r[['route_guid', 'agent_guid','qa_status']], on='route_guid', how='inner')
s = pd.merge(s, r[['route_guid', 'agent_guid','qa_status']], on='route_guid', how='inner')

srnm = pd.merge(srn,s,left_on='id',right_on='student_id',how='inner')
#%%

client = boto3.client('rekognition')

rekognition = boto3.client('rekognition', region_name='eu-west-1')
dynamodb = boto3.client('dynamodb', region_name='eu-west-1')
s3 = boto3.resource('s3',region_name='eu-west-1')
my_bucket = s3.Bucket('scholartransport')
i=0
f = open('c:/Users/flip/Documents/GDE/facesschool.csv','w')
f.write('EMIS_NUMBER;LEARNER_GUID;PHOTONAME\n')

for index, row in srnm.iterrows():
    fname = row['photoname']
    #if row['emis'] != row['emis_number'] and row['emis']=='700251785':
    if row['emis'] == '700251785':
        #print(row['photoname'])
        if (fname.find('_IN_') >= 0 or fname.find('_OUT_') >= 0):
            print(fname)
            emisnumber = row['emis_number']
            s3.Bucket('scholartransport').download_file(fname, 'rekon.jpg')
            print(row['emis'])
            print(row['emis_number'])
            try:
                with open('rekon.jpg', 'rb') as image:
                    response = client.search_faces_by_image(
                        CollectionId=emisnumber,
                        FaceMatchThreshold=99,
                        Image={'Bytes': image.read()})
                print(response)
                faceMatches = response['FaceMatches']
                print('Matching faces')
                for match in faceMatches:
                    print('FaceId:' + match['Face']['FaceId'])
                    print('ExternalImageId:' + match['Face']['ExternalImageId'])
                    studentrekognitionid = match['Face']['ExternalImageId']
                    print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
                    print
            except:
                print('Error....')

            #input('press enter...')

            print('{0}:{1}:{2}'.format(emisnumber,studentrekognitionid,fname))
            f.write('{0}:{1}:{2}\n'.format(emisnumber,studentrekognitionid,fname))

        if i % 50 == 0:
            f.flush()
            print('Flush....', i)
        i += 1
    #if i>20:
        #break
f.close()




# In[20]:
b.sort_values('stop_date', inplace=True)
s.sort_values('capture_date', inplace=True)
sb = pd.merge_asof(s, b, left_on='capture_date',right_on = 'stop_date', by='route_guid', direction='forward')

# In[109]:

sb.to_csv('c:/Users/flip/Documents/GDE/Bus/sb.csv')

# In[26]:
sbg=sb.route_guid.value_counts()
sbgs=sb.groupby(['route_guid','stop_guid_y','lat_start','lon_start'])

#%%
s['lat']=s.lat.str.replace(',', '.')
s['lon']=s.lon.str.replace(',', '.')
#s['capture_date'] = pd.to_datetime(s.photo_date + ' ' + s.photo_time)
#%%

s['lat'] = pd.to_numeric(s.lat)
s['lon'] = pd.to_numeric(s.lon)
#%%
s.rename(columns={'stop number reviewed': 'stop_number_reviewed'}, inplace=True)
s.sort_values(['routeguid_table','stopguid_table','stop_number_reviewed'], inplace=True)

g = s.routeguid_table.value_counts()
#%%
for name, group in sbgs.groupby(['route_guid','stop_guid_y','lat_start','lon_start']):
    print(name)
#%%
for i in g.items():
    route = i[0]
    print(route)
#%%

colors = [
    'red',
    'blue',
    'gray',
    'darkred',
    'lightred',
    'orange',
    'beige',
    'green',
    'darkgreen',
    'lightgreen',
    'darkblue',
    'lightblue',
    'purple',
    'darkpurple',
    'pink',
    'cadetblue',
    'lightgray',
    'black'
]
c = 1
m = folium.Map([-26.5973689, 27.8349605], zoom_start=12)
for i in g.items():
    route = i[0]
    line = []
    print(route)
    if c == 16:
        break
    for index, row in s[s.routeguid_table == route].iterrows():
        p = [row['lat'], row['lon']]
        print(p)
        line.append([row['lat'], row['lon']])
        poptxt = str(row['routeguid_table']) + ' ' + str(row['stop_number_reviewed'])
        color = colors[c]
        folium.Marker(location=p,
            popup=poptxt,
            icon=folium.Icon(color=color)).add_to(m)
    folium.PolyLine(line, popup=route, color=colors[c]).add_to(m)
    c+=1
    break
m.save('c:/Users/flip/Documents/GDE/Bus/sb.html')


#%%

m = folium.Map([-26.5973689, 27.8349605], zoom_start=12)
oldroute = 0
line = []
for i, j in g.items():
    route = i[0]
    routestop = i[1]
    if route != oldroute:
        if oldroute != 0:
            folium.PolyLine(line, popup=oldroute).add_to(m)
        oldroute = route
        line = []
    for index, row in sb[val].iterrows():
        if row['route_guid'] == route and row['stop_number'] == i[1]:
            p = [row['lat_start'], row['lon_start']]
            line.append([row['lat_start'], row['lon_start']])
            poptxt = str(row['route_guid']) + ' ' + str(routestop) + ' ' + str(j)
            color = 'green'
            if routestop == '1':
                color = 'red'
            folium.Marker(location=p,
                          popup=poptxt,
                          icon=folium.Icon(color=color)).add_to(m)

# In[30]:
g=s.route_guid.value_counts()
for i,j in g.items():
    route = i
    nogps=0
    for index, row in s[s.route_guid == route].iterrows():
        if row['lat'] == 0:
            nogps=nogps+1
    if nogps > 0:
        print('Route : {0} , has {1} records without gps coords'.format(route,nogps))

#%%
for index, row in l.iterrows():
    tmp = s[s.student_rekognition_id == row['learner_guid']]
    l.at[i, 'disembark_route'] = tmp.iloc[0].route_guid
    l.at[i, 'disembark_route_time'] = s[s.student_rekognition_id == row['learner_guid']]



#%%


tmpg.sort_values('student_id', ascending=False).drop_duplicates(['route_guid', 'emis_number'])


# In[35]:


tmp = s.groupby(['route_guid', 'emis_number', 'on_off'])['student_id'].count().max(level=0)


# In[52]:


stemp = s.agent_guid == '132'
btemp = b.agent_guid == '132'
rtemp = r.agent_guid == '132'


# In[ ]:


for index, row in a.iterrows():
    stemp = s.agent_guid == row['agent_guid']
    btemp = b.agent_guid == row['agent_guid']
    rtemp = r.agent_guid == row['agent_guid']
    sbtemp = pd.merge_asof(s[stemp], b[btemp], on='capture_date', by='route_guid', direction='nearest')

# In[69]:

#%%

sb = pd.merge_asof(s.sort_values('capture_date'), b.sort_values('capture_date'), on='capture_date', by='route_guid',
                   direction='nearest')

# In[30]:


sb[sb.route_guid == '3Z594B5DQAZ620190417_134524']


# In[43]:


val = (sb.emis_number == '700231530') & (sb.route_guid.str.contains('20190417'))


# In[65]:


sbg = sb[val].groupby(['route_guid', 'stop_number', 'emis_number'])['student_id'].count()

# In[28]:


sbtemp.groupby(['route_guid', 'stop_number', 'emis_number', 'on_off'])['student_id'].count()

# In[18]:


gt = sbtemp.groupby(['route_guid', 'stop_number'])['student_id'].count()

# In[66]:


sbg

# In[67]:


for i, j in sbg.items():
    print(i, j)

# # MAPS

# In[118]:


colors = [
    'red',
    'blue',
    'gray',
    'darkred',
    'lightred',
    'orange',
    'beige',
    'green',
    'darkgreen',
    'lightgreen',
    'darkblue',
    'lightblue',
    'purple',
    'darkpurple',
    'pink',
    'cadetblue',
    'lightgray',
    'black']

c = 1
m = folium.Map([-26.5973689, 27.8349605], zoom_start=12)
line = []
pcnt = 0
for i, j in sbg.items():
    route = i[0]
    school = i[2]
    for index, row in sb.iterrows():
        if row['route_guid'] == route and row['stop_number'] == routestop:
            pcnt += 1
            p = [row['lat_start'], row['lon_start']]
            line.append([row['lat_start'], row['lon_start']])
            poptxt = str(row['route_guid']) + ' ' + str(routestop) + ' ' + str(j)
            color = colors[c]
            if routestop == '1':
                color = 'red'
            folium.Marker(location=p,
                          popup=poptxt,
                          icon=folium.Icon(color=color)).add_to(m)
            print(oldroute, route, routestop, pcnt, line)
            if oldroute != route and oldroute:
                if pcnt > 1:
                    print(line)
                    folium.PolyLine(line, popup=oldroute, color=colors[c]).add_to(m)
                    pcnt = 0
                line = []
                oldroute = route
                c += 1
                pcnt = 0

# In[119]:


m

# In[75]:


m.save('c:/Users/flip/Documents/GDE/Bus/700231530.html')

# In[62]:


m = folium.Map([-26.5973689, 27.8349605], zoom_start=12)
oldroute = 0
line = []
for i, j in sbg.items():
    route = i[0]
    routestop = i[1]
    if route != oldroute:
        if oldroute != 0:
            folium.PolyLine(line, popup=oldroute).add_to(m)
        oldroute = route
        line = []
    for index, row in sb[val].iterrows():
        if row['route_guid'] == route and row['stop_number'] == i[1]:
            p = [row['lat_start'], row['lon_start']]
            line.append([row['lat_start'], row['lon_start']])
            poptxt = str(row['route_guid']) + ' ' + str(routestop) + ' ' + str(j)
            color = 'green'
            if routestop == '1':
                color = 'red'
            folium.Marker(location=p,
                          popup=poptxt,
                          icon=folium.Icon(color=color)).add_to(m)

# In[21]:


m

# In[ ]:


pd.set_option('max_columns', 1000)
now = datetime.datetime.now()
print("Downloading Sites .......")
SQL = "SELECT b.*,r.route_date FROM BUS_STOPS b,ROUTES r where b.route_guid = r.route_guid"
# SQLHSS="SELECT * FROM HSS_APPLICANTS"
connection = cx_Oracle.connect("scholar", "scholar123", "130.61.26.162/PDB1.svcsubnetad1.svcvcn.oraclevcn.com")
b = pd.read_sql(SQL, con=connection)
b['DT'] = b[['ROUTE_DATE', 'START_TIME']].apply(lambda x: ' '.join(x), axis=1)
b['DT'] = b['DT'].apply(np.datetime64)

# In[ ]:


b = b.fillna('NV')


# In[ ]:


def make_clickable(val):
    # target _blank to open new window
    return '<a target="_blank" href="{}">{}</a>'.format(val, val)


# In[ ]:


b['PHOTO1'] = 'https://s3.amazonaws.com/scholartransport/' + b.STOP_PHOTO_1

# In[ ]:


b.style.format({'PHOTO1': make_clickable})


# In[ ]:


def path_to_image_html(path):
    return '<img src="' + path + '" width="260" >'


pd.set_option('display.max_colwidth', -1)

# In[ ]:


HTML(b[['STOP_GUID', 'PHOTO1']].to_html(escape=False, formatters=dict(PHOTO1=path_to_image_html)))

# In[17]:


get_ipython().system('pip install ipyleaflet')

# In[121]:


r126 = r.AGENT_GUID == '126'

# In[122]:


r126.sum()

# In[123]:


r.dtypes

# In[ ]:


b = pd.read_csv('g:/gde/Bus/bus_stops.csv', dtype='str')
r = pd.read_csv('g:/gde/Bus/routes.csv', dtype='str')
s = pd.read_csv('g:/gde/Bus/student_rekognition.csv', dtype='str')
b.index = pd.to_datetime(b['STOP_DATE'])
b.head()
b.shape
s = pd.merge(s, r[['ROUTE_GUID', 'AGENT_GUID']], on='ROUTE_GUID', how='inner')
sb125.iloc[0]
s125 = s[s['AGENT_GUID'] == '125']
s125
s['CAPTURE_DATE'] = pd.to_datetime(s.GPS_DATE)
s = s[['CAPTURE_DATE', 'STUDENT_ID', 'ROUTE_GUID', 'EMIS_NUMBER']]
r['CAPTURE_DATE'] = pd.to_datetime(r.ROUTE_DATE + ' ' + r.START_TIME)
r = r[['CAPTURE_DATE', 'ROUTE_GUID', 'AGENT_GUID']]
r.iloc[0]
b = b[['CAPTURE_DATE', 'ROUTE_GUID', 'STOP_GUID']]
r.head()
b['CAPTURE_DATE'] = pd.to_datetime(b['STOP_DATE'])
keys = b['CAPTURE_DATE'].dt.round('T')
keys
b.groupby([keys]).count()
keys.shape
sb125 = pd.merge_asof(s125, b125, on='CAPTURE_DATE', by='ROUTE_GUID', direction='nearest')
s.sort_values('CAPTURE_DATE', inplace=True)
sb125.groupby(['ROUTE_GUID', 'STOP_GUID_y'])['STUDENT_ID'].count()

