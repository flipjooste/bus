# coding: utf-8

# In[1]:


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


s = pd.read_csv('c:/Users/flip/Documents/GDE/Bus/student_rekognition.csv', dtype='str', encoding='ANSI')

# In[95]:


b = pd.read_csv('c:/Users/flip/Documents/GDE/Bus/bus_stops.csv', dtype='str')

# In[96]:
r = pd.read_csv('c:/Users/flip/Documents/GDE/Bus/routes.csv', dtype='str')


# In[98]:

new = b.start_gps.str.split(',', n=1, expand=True)
b['lat_start'] = pd.to_numeric(new[0])
b['lon_start'] = pd.to_numeric(new[1])

# In[99]:


s = s.fillna('na')
r = r.fillna('na')
b = b.fillna('na')

# In[100]:


s.columns = map(str.lower, s.columns)
r.columns = map(str.lower, r.columns)
b.columns = map(str.lower, b.columns)

# In[101]:


s['gps_time'] = s.gps_time.str.split('.JPG', expand=True)[0]
s['gps_time'] = s.gps_time.str.replace('_', ' ')
s['gps_time'] = s.gps_time.str.replace('v', '')

# In[102]:


s['capture_date'] = pd.to_datetime(s.gps_time)

# In[103]:


s.sort_values('capture_date', inplace=True)

# In[110]:
tmp = (b.stop_date == 'na') & (b.start_date != 'na')
b['stop_date'] = b[tmp]['start_date']

#%%

b = b[b.stop_date != 'na']
#%%

r = r[r.start_time!= 'na']

# In[111]:
r['capture_date'] = pd.to_datetime(r.route_date + ' ' + r.start_time)
#b['stop_date'] = pd.to_datetime(b['stop_date'])
#b['start_date'] = pd.to_datetime(b['start_date'])

b.sort_values('stop_date', inplace=True)
#%%
r['start_date']=r['capture_date']


# In[105]:


r.sort_values('capture_date', inplace=True)

# In[92]:


s.index = s.capture_date
b.index = b.capture_date
r.index = r.capture_date

# In[8]:


b = pd.merge(b, r[['route_guid', 'agent_guid','qa_status']], on='route_guid', how='inner')

# In[76]:


s = pd.merge(s, r[['route_guid', 'agent_guid','qa_status']], on='route_guid', how='inner')

# In[20]:


sb = pd.merge_asof(s, b, left_on='capture_date',right_on = 'start_date', by='route_guid', direction='backward')

# In[109]:


b[['start_date', 'stop_date']].to_csv('g:/gde/bus/gpstime.csv')

# In[26]:

r.dtypes

#%%


tmpg = s.groupby(['route_guid', 'emis_number'])['student_id'].count()

# In[27]:


tmpg = tmpg.to_frame()
tmpg = tmpg.reset_index()

# In[28]:


tmpg

# In[29]:


tmpg = tmpg.sort_values(by='student_id', ascending=False)

# In[30]:


tmpg.sort_values('student_id', ascending=False).drop_duplicates(['route_guid', 'emis_number'])

# In[37]:


tval = tmpg.route_guid == 'LGV8YWNHIO0C20190402_151130'

# In[38]:


tmpg[tval]

# In[35]:


tmp = s.groupby(['route_guid', 'emis_number', 'on_off'])['student_id'].count().max(level=0)

# In[23]:


sp = sp.fillna('na')

# In[24]:


sp['sdate'] = sp.student_rekognition_id.str.split('_', expand=True)[0].str[-8:]

# In[26]:


sp['cnt'] = 1

# In[27]:


same = sp.sdate == sp.rdate

# In[28]:


notsame = sp.sdate != sp.rdate

# In[29]:


sp[notsame].to_csv('g:/gde/Bus/notsame.csv')

# In[30]:


sp[same].to_csv('g:/gde/Bus/same.csv')

# In[33]:


sp[notsame].shape

# In[30]:


s = s.fillna('na')

# In[29]:


sna = s.capture_date == 'na'

# In[62]:


s[sna]

# In[136]:


s.groupby(s.sdate)['cnt'].count().to_clipboard()

# In[87]:


s[same].to_csv('g:/gde/Bus/sr_csv')

# In[52]:


stemp = s.agent_guid == '132'
btemp = b.agent_guid == '132'
rtemp = r.agent_guid == '132'

# In[53]:


sbtemp = pd.merge_asof(s[stemp], b[btemp], on='capture_date', by='route_guid', direction='nearest')

# In[36]:


a = pd.read_csv('g:/gde/Bus/agent.csv', dtype='str')

# In[37]:


a.columns = map(str.lower, a.columns)

# In[38]:


a.loc[0]

# In[ ]:


for index, row in a.iterrows():
    stemp = s.agent_guid == row['agent_guid']
    btemp = b.agent_guid == row['agent_guid']
    rtemp = r.agent_guid == row['agent_guid']
    sbtemp = pd.merge_asof(s[stemp], b[btemp], on='capture_date', by='route_guid', direction='nearest')

# In[69]:


sb = pd.merge_asof(s.sort_values('capture_date'), b.sort_values('capture_date'), on='capture_date', by='route_guid',
                   direction='nearest')

# In[30]:


val = sb.route_guid == '3Z594B5DQAZ620190417_134524'

# In[43]:


val = (sb.emis_number == '700231530') & (sb.route_guid.str.contains('20190417'))

# In[34]:


sb[val].head()

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
    'black'
]
c = 1
m = folium.Map([-26.5973689, 27.8349605], zoom_start=12)
oldroute = ''
line = []
pcnt = 0
for i, j in sbg.items():
    route = i[0]
    routestop = i[1]
    school = i[2]
    for index, row in b.iterrows():
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

