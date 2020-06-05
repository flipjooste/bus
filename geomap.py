from shapely.geometry import mapping
from shapely.wkt import loads
from fiona import collection
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

df = pd.read_csv('c:/Users/Flip/Documents/NDPW/OldProject/allBuildings.csv',sep=',')
df.columns
df.columns = map(str.lower, df.columns)
dfp = pd.read_csv('c:/Users/Flip/Documents/NDPW/OldProject/RestorePolygonAttribute.csv',sep=';')
dfp.columns = map(str.lower, dfp.columns)

dfa = pd.read_csv('c:/Users/Flip/Documents/NDPW/OldProject/RestoreAttribute.csv',sep=';')
dfa.columns = map(str.lower, dfa.columns)

#gf=gpd.read_file('c:/Users/Flip/Documents/NDPW/OldProject/qa.shp')

df.columns

