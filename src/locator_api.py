# Libraries
import pandas as pd
import requests
import json
import yaml
import joblib

# Geoanalytics
import geopandas as gpd
from shapely.geometry import Point


###############CONFIG FILE#############################
#Reading from config file
def load_conf_file(config_file):
   with open(config_file, "r") as f:
       config = yaml.safe_load(f)
   return config

#Calling the function and defining variables
config = load_conf_file("./config/settings.yml")
df_cusec = joblib.load('./obj/df_cusec_reduced_geometry.pkl')
df_cusec['geometry_cusec'] = df_cusec['geometry']

token = config["MAPQUEST"]["TOKEN"]

#Let's define a function where we get the latitud and longitud from the address
def locator(df_input):
    #Mapquest parametersd
    direccion = df_input['direccion'].values[0]
    url = 'http://www.mapquestapi.com/geocoding/v1/address?key={0}&location={1}'.format(token, direccion)
    #Let's call the function
    response = requests.get(url).content
    dict_from_json = json.loads(response)
    for i in range(len(dict_from_json['results'][0]['locations'])):
        if dict_from_json['results'][0]['locations'][i]['postalCode'][0:3] == df_input['codigo_postal'].values[0][0:3]:
            latitud = dict_from_json['results'][0]['locations'][i]['latLng']['lat']
            longitud = dict_from_json['results'][0]['locations'][i]['latLng']['lng']
            break
        else:
            latitud = 'NaN'
            longitud = 'NaN'

    df = pd.DataFrame({'direccion': [df_input['direccion'].values[0]],
                       'latitud': [latitud],
                       'longitud': [longitud]})
    return df

#Let's assign a CUSEC to the spatial point
def assign_cusec(df):
    if df['longitud'].values[0] != 'NaN':
        print("Localizado")
        crs={'init': 'epsg:4326'} #'EPSG:4326'
        df[['latitud', 'longitud']] = df[['latitud', 'longitud']].astype(float)
        df["geometry"] = df.apply(lambda x: Point(x.longitud, x.latitud), axis=1)
        df = gpd.GeoDataFrame(df, crs=crs)
        # Geospatial join between geodataframe that contains a point and geodataframe that contains a polygon
        df = gpd.sjoin(df, df_cusec[['CUSEC','precio_m2','geometry','geometry_cusec']],op="within").\
            drop(columns=['index_right','geometry']).\
            rename(columns={'geometry_cusec':'geometry'})
        if df.shape[0] == 0:
            print("Lugar fuera de área")
    else:
        print("No localizado")
        #df[['CUSEC''precio_m2','geometry']] = pd.DataFrame([['NaN', 'NaN','NaN']])
    return df
