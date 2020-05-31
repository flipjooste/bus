#%%
import pandas as pd

df = pd.read_csv('c:/Users/Flip/Documents/NDPW/ChangeLog.csv',sep=';')
df.columns = map(str.lower, df.columns)
bld = df.table_name == 'BUILDINGS'
dfb = df[bld]
dfb=dfb.drop(['change_log_id','table_name','action','action_by','action_source','action_on'], axis = 1)
g = dfb.groupby(['record_id'])
#%%
i=0
fname=[]
fval=[]
db = pd.DataFrame()
for group_name, group in g:
     fname=[]
     fval = []
     fname.append('record_id')
     fval.append(group_name)
     for row_index, row in group.iterrows():
         col = row['field_name']
         column_type = row['value']
         #print(col,column_type)
         fname.append(row[1])
         fval.append([row[2]])
         #print('{0};{1};{2}'.format(group_name,col, column_type))
     data = dict(zip(fname, fval))
     dt = pd.DataFrame(data)
     db = db.append(dt, sort = True)
     print(dt.head())
     i+=1
     #if i>100:
        #break



#%%
from shapely.geometry import mapping
from shapely.wkt import loads
from fiona import collection
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

df = pd.read_csv('c:/Users/Flip/Documents/NDPW/OldProject/DelBuildings.csv',sep=';')
df.columns
df.columns = map(str.lower, df.columns)
gf=gpd.read_file('c:/Users/Flip/Documents/NDPW/OldProject/qa.shp')
from shapely.geometry import Polygon

df.polygo#%%

i=0
fname=[]
fval=[]
db = pd.DataFrame()
for group_name, group in g:
    fname=[]
    fname.append('record_id')
    fval.append(group_name)
    for row_index, row in group.iterrows():
        col = row['field_name']
        column_type = row['value']
        fname.append(row[1])
        fval.append([row[2]])
        #print('{0};{1};{2}'.format(group_name,col, column_type))
    data = dict(zip(fname, fval))
    dt = pd.DataFrame(data)
    db = db.append(dt, sort = True)
    print(dt.head())
    i+=1
    if i>10:
        break
g
import pandas as pd
df = pd.read_csv('c:/Users/Flip/Documents/NDPW/ChangeLog.csv',sep=';')
df.columns = map(str.lower, df.columns)
bld = df.table_name == 'BUILDINGS'
dfb = df[bld]
dfb=dfb.drop(['change_log_id','table_name','action','action_by','action_source','action_on'], axis = 1)
g = dfb.groupby(['record_id'])
g
i=0
fname=[]
fval=[]
db = pd.DataFrame()
for group_name, group in g:
    fname=[]
    fname.append('record_id')
    fval.append(group_name)
    for row_index, row in group.iterrows():
        col = row['field_name']
        column_type = row['value']
        fname.append(row[1])
        fval.append([row[2]])
        #print('{0};{1};{2}'.format(group_name,col, column_type))
    data = dict(zip(fname, fval))
    dt = pd.DataFrame(data)
    db = db.append(dt, sort = True)
    print(dt.head())
    i+=1
    if i>10:
        break
dbf
dfb
g = dfb.groupby(['record_id'])
g
print(g)
g[0]
g.record_id
g.size()
for group_name, group in g:
    print(group)
for group_name, group in g:
    print(group_name,group)
    break
for group_name, group in g:
    print(group_name,group[0])
    break
i=0
fname=[]
fval=[]
db = pd.DataFrame()
for group_name, group in g:
    fname=[]
    fname.append('record_id')
    fval.append(group_name)
    for row_index, row in group.iterrows():
        col = row['field_name']
        column_type = row['value']
        print(col,column_type)
        fname.append(row[1])
        fval.append([row[2]])
        #print('{0};{1};{2}'.format(group_name,col, column_type))
    data = dict(zip(fname, fval))
    dt = pd.DataFrame(data)
    db = db.append(dt, sort = True)
    print(dt.head())
    i+=1
    if i>10:
        break
i=0
fname=[]
fval=[]
db = pd.DataFrame()
for group_name, group in g:
    fname=[]
    fval = []
    fname.append('record_id')
    fval.append(group_name)
    for row_index, row in group.iterrows():
        col = row['field_name']
        column_type = row['value']
        print(col,column_type)
        fname.append(row[1])
        fval.append([row[2]])
        #print('{0};{1};{2}'.format(group_name,col, column_type))
    data = dict(zip(fname, fval))
    dt = pd.DataFrame(data)
    db = db.append(dt, sort = True)
    print(dt.head())
    i+=1
    if i>10:
        break
i=0
fname=[]
fval=[]
db = pd.DataFrame()
for group_name, group in g:
    fname=[]
    fval = []
    fname.append('record_id')
    fval.append(group_name)
    for row_index, row in group.iterrows():
        col = row['field_name']
        column_type = row['value']
        print(col,column_type)
        fname.append(row[1])
        fval.append([row[2]])
        #print('{0};{1};{2}'.format(group_name,col, column_type))
    data = dict(zip(fname, fval))
    dt = pd.DataFrame(data)
    db = db.append(dt, sort = True)
    print(dt.head())
    i+=1
    if i>100:
        break
i=0
fname=[]
fval=[]
db = pd.DataFrame()
for group_name, group in g:
    fname=[]
    fval = []
    fname.append('record_id')
    fval.append(group_name)
    for row_index, row in group.iterrows():
        col = row['field_name']
        column_type = row['value']
        #print(col,column_type)
        fname.append(row[1])
        fval.append([row[2]])
        #print('{0};{1};{2}'.format(group_name,col, column_type))
    data = dict(zip(fname, fval))
    dt = pd.DataFrame(data)
    db = db.append(dt, sort = True)
    print(dt.head())
    i+=1
    #if i>100:
    #break
db.to_csv('c:/Users/Flip/Documents/NDPW/DelBuildings.csv',sep=';')
import geopandas as gpd
df = pd.read_csv('c:/Users/Flip/Documents/NDPW/DelBuildings.csv',sep=';')
df = pd.read_csv('c:/Users/Flip/Documents/NDPW/OldProject/DelBuildings.csv',sep=';')
df.columns
df.columns = map(str.lower, df.columns)
from shapely.geometry import Polygon
df.polygon
from shapely.geometry import LineString
rec = df.record_id == '200750515'
df[rec]
rec = df.record_id == 200750515
df[rec]
df.polygon
df[rec].polygon
df[rec].polygon.str.split(';')
stmp = df[rec].polygon.str.split(';')
stmp
stmp[0]
stmp
print(df[rec].polygon)
print(df[rec].polygon.str.split(';'))
df[['pol']] = pd.DataFrame([ x.split(';') for x in df['pol'].tolist() ])
df1[['pol']] = pd.DataFrame([ x.split(';') for x in df['polygon'].tolist() ])
df.columns
df1[['pol']] = pd.DataFrame([ x.split(';') for x in df['polygon'].tolist() ])
df.dtypes
df1[['pol']] = pd.DataFrame([ x.split(';') for x in df.polygon.tolist() ])
df1[['pol']] = pd.DataFrame([ x.split(';') for x in df.polygon.tolist()])
split_data = df[rec].polygon.str.split(';')
data = split_data.to_list()
data
data[0]
data[1]
data[1:]
data[:1]
for d in data:
    print(d)
for d,e in data:
    print(e)
split_data
line = LineString(data)
line = LineString(split_data)
new = df.polygon.str.split(";", n = 1, expand = True)
new = df[rec].polygon.str.split(";", n = 1, expand = True)
new
new = df[rec].polygon.str.split(";",  expand = True)
new
new[0]
new[1]
for n in new:
    print(n)
new.columns
new.head()
pd.set_option('display.max_columns', 50)
new.head()
df.columns
new.columns
new.items()
new.first()
history
df['geopoly'] = df.polygon.str.split(";",  expand = True)
df = df.fillna('nv')
df['geopoly'] = df.polygon.str.split(";",  expand = True)
df = df.fillna('0;0')
df['geopoly'] = df.polygon.str.split(";",  expand = True)
history
df = pd.read_csv('c:/Users/Flip/Documents/NDPW/OldProject/DelBuildings.csv',sep=';')
df.columns
df.columns = map(str.lower, df.columns)
from shapely.geometry import Polygon
df.polygon
from shapely.geometry import LineString
df=df.fillna('0;0')
df['geopoly'] = df.polygon.str.split(";",  expand = True)
df.columns
df['geopoly'] = df.polygon.str.split(";")
df.columns
df.geopoly
df1['geometry'] = df['geopoly'].apply(lambda g: wkt.loads(g))
import shapely
df1['geometry'] = df['geopoly'].apply(lambda g: wkt.loads(g))
from shapely.geometry import mapping
from shapely.wkt import loads
from fiona import collection
df1['geometry'] = df['geopoly'].apply(lambda g: wkt.loads(g))
df[rec]
df[rec].geopoly
p=df[rec].geopoly
p
p=df[rec].geopoly.to_list()
p
gdf = geopandas.GeoDataFrame(
    df, geometry=geopandas.points_from_xy(df.geopoly))
import geopandas
gdf = geopandas.GeoDataFrame(
    df, geometry=geopandas.points_from_xy(df.geopoly))
df['Coordinates'] = df['geopoly'].apply(wkt.loads)
from shapely import wkt
df['Coordinates'] = df['geopoly'].apply(wkt.loads)
from geomet import wkt
import json
#your WKT input:
ls = 'LINESTRING(2.379444 48.723333, 2.365278 48.720278, 2.2525 48.696111, 2.224167 48.69, 2.129167 48.652222, 2.093611 48.638056)'
ls = 'LINESTRING(2.379444 48.723333, 2.365278 48.720278, 2.2525 48.696111, 2.224167 48.69, 2.129167 48.652222, 2.093611 48.638056)'
ls
ls_json = wkt.loads(ls)
ls_json
from geojson import Polygon
Polygon([[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)]])
Polygon(p)
p
p[0]
p[1]
df[rec].polygon
df[rec].polygon.to_list()
p1=df[rec].polygon.to_list()
p1
p1[0]
p1=df[rec].polygon.to_string()
p1
p1[0]
p1=df[rec].geopoly.to_string()
p1
p
str(p)
s=str(p)
s
s[0]
s[1]
s.replace('[','')
s.replace(']','')
s=s.replace('[','')
s=s.replace(']','')
s
s.replace("'",'')
s[0]
s=s.replace("'",'')
s[0]
import shapely.wkt
import shapely.geometry
list_wkt = ['POLYGON ((-88.131229288 41.900200029,-88.12973798 41.900104202,-88.129785999 41.894907769,-88.131352409 41.895051521,-88.131229288 41.900200029))', 'POLYGON ((-88.121359263 41.887694051,-88.12027565 41.887654116,-88.120264921 41.884451192,-88.11968556399999 41.884483142,-88.11962119099999 41.882669946,-88.121251974 41.882637995,-88.121359263 41.887694051))']
list_polygons =  [shapely.wkt.loads(poly) for poly in list_wkt]
print( shapely.geometry.MultiPolygon(list_polygons) )
list_wkt
list_wkt = ['POLYGON ((-88.131229288 41.900200029,-88.12973798 41.900104202,-88.129785999 41.894907769,-88.131352409 41.895051521,-88.131229288 41.900200029))']
list_wkt
list_polygons =  [shapely.wkt.loads(poly) for poly in list_wkt]
list_polygons
p
p1
p1=p1.replace(',',' ')
p1
history
p1=df[rec].polygon.to_string()
p1
p1=p1.replace(',',' ')
p1
p1=p1.replace(';',',')
p1
p1[5:]
p1[7:]
p1=p1[7:]
p11
p1
history
p1=df[rec].polygon.to_string()
p1=df[rec].polygon.to_list()
p1
p1[0]
t=p1[0]
t=t.replace(',',' ')
t=t.replace(';',',')
t
'POLYGON((' + t + '))'
t
t='POLYGON((' + t + '))'
t
list_wkt =[t]
list_wkt
list_polygons =  [shapely.wkt.loads(poly) for poly in list_wkt]
list_wkt=[]
list_wkt.append(t)
list_wkt
list_polygons =  [shapely.wkt.loads(poly) for poly in list_wkt]
list_wkt = ['POLYGON ((23.341449536383152 -34.053386656967945,23.341363705694675 -34.05359777079189,23.3418994769454 -34.05375138354648,23.34216568619013 -34.05371916100259,23.3420842140913 -34.05353499226232,23.34194742143154 -34.053562492597365))']
list_polygons =  [shapely.wkt.loads(poly) for poly in list_wkt]
list_wkt = ['POLYGON ((-88.131229288 41.900200029,-88.12973798 41.900104202,-88.129785999 41.894907769,-88.131352409 41.895051521,-88.131229288 41.900200029))', 'POLYGON ((-88.121359263 41.887694051,-88.12027565 41.887654116,-88.120264921 41.884451192,-88.11968556399999 41.884483142,-88.11962119099999 41.882669946,-88.121251974 41.882637995,-88.121359263 41.887694051))']
list_polygons =  [shapely.wkt.loads(poly) for poly in list_wkt]
list_wkt = ['POLYGON ((-88.131229288 41.900200029,-88.12973798 41.900104202,-88.129785999 41.894907769,-88.131352409 41.895051521,-88.131229288 41.900200029))']
list_polygons =  [shapely.wkt.loads(poly) for poly in list_wkt]
list_wkt1 = ['POLYGON ((23.341449536383152 -34.053386656967945,23.341363705694675 -34.05359777079189,23.3418994769454 -34.05375138354648,23.34216568619013 -34.05371916100259,23.3420842140913 -34.05353499226232,23.34194742143154 -34.053562492597365))']
list_wkt1
list_polygons =  [shapely.wkt.loads(poly) for poly in list_wkt]
list_polygons =  [shapely.wkt.loads(poly) for poly in list_wkt1]
list_wkt1 = ['POLYGON ((23.341449536383152 -34.053386656967945,23.341363705694675 -34.05359777079189,23.3418994769454 -34.05375138354648,23.34216568619013 -34.05371916100259,23.3420842140913 -34.05353499226232,23.34194742143154 -34.053562492597365,23.341449536383152 -34.053386656967945))']
list_polygons =  [shapely.wkt.loads(poly) for poly in list_wkt1]
list_polygons
list_polygons.geom_type
list_polygons.geom_type()
list_polygons.geom_type
list_polygons
list_polygons.area()
list_polygons.area
for poly in list_wkt1:
    print(poly)
shapely.wkt.loads(poly)
p1=df[rec].polygon.to_list()
shapely.wkt.loads(p1)
t=p1[0]
t=t.replace(',',' ')
t=t.replace(';',',')
t
t='POLYGON((' + t + '))'
t
shapely.wkt.loads(t)
t
t1='POLYGON((23.341449536383152 -34.053386656967945,23.341363705694675 -34.05359777079189,23.3418994769454 -34.05375138354648,23.34216568619013 -34.05371916100259,23.3420842140913 -34.05353499226232,23.34194742143154 -34.053562492597365,23.341449536383152 -34.053386656967945))'
shapely.wkt.loads(t1)
df[rec]['polygon'].map(lambda polygon: shapely.ops.transform(lambda x, y: (y, x), shapely.wkt.loads(t1)))
df[rec].polygon
dft = df[rec]['polygon'].map(lambda polygon: shapely.ops.transform(lambda x, y: (y, x), shapely.wkt.loads(t1)))
dft
dft = df[rec]['polygon'].map(lambda polygon: shapely.ops.transform(lambda x, y: (y, x), shapely.wkt.loads(t1)))
geometry = df['polygon'].map(shapely.wkt.loads(t1))
geometry = shapely.wkt.loads(t1)))
geometry = shapely.wkt.loads(t1)
geometry
df['polygons'] = df['polygons'].apply(lambda g: wkt.loads(t1))
df['polygons'] = df['polygons'].apply(lambda t1: wkt.loads(t1))
df1
t1
df[rec].polygon = t1
df[rec].polygon
t1
gdf = geopandas.GeoDataFrame(df[rec], geometry=t1)
t1
df['Footprint'].map(lambda polygon: shapely.ops.transform(lambda x, y: (y, x), shapely.wkt.loads(t1)))
df['polygon'].map(lambda polygon: shapely.ops.transform(lambda x, y: (y, x), shapely.wkt.loads(t1)))
df[rec]
df[rec]
df[rec].polygon
gdf = geopandas.GeoDataFrame(df, geometry='polygons')
gdf = geopandas.GeoDataFrame(df, geometry='polygon')
df[rec].polygon
df[rec].polygon = t1
t1
df[rec]['polygon'] = t1
df[rec].polygon
dft1=df[rec]
dft1.polygon=t1
dft1
df[rec]
history
from shapely.geometry import mapping
from shapely.wkt import loads
from fiona import collection
df = pd.read_csv('c:/Users/Flip/Documents/NDPW/OldProject/DelBuildings.csv',sep=';')
df.columns
df.columns = map(str.lower, df.columns)
from shapely.geometry import Polygon
df.polygon
from shapely.geometry import LineString
df.dtypes
rec = df.record_id == 200750515
df[rec]
df[rec].polygon
dft1=df[rec]
dft1
t1
dft1['polygon'] = t1
dft1
dft1.polygon
gdf = geopandas.GeoDataFrame(df, geometry='polygon')
t1
df['Coordinates'] = df['polygons'].apply(wkt.loads)
df['polygon'] = df['polygon'].apply(wkt.loads)
dft1['polygon'] = dft1['polygon'].apply(wkt.loads)
dft1['polygon'].apply(wkt.loads)
dft1['polygon'].apply(wkt.loads)
history
from shapely.geometry import LineString