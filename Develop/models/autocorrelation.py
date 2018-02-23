import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
from sodapy import Socrata
from geopandas import gpd

client = Socrata("data.cityofchicago.org", 'EjrjYzG6YAkBx7bPBzME8jD4c')
results = client.get("w3hi-cfa4",limit = 500000)

complaints = pd.DataFrame.from_records(results)

split = complaints['beat'].str.split('|').apply(pd.Series, 1).stack()
split.index = split.index.droplevel(-1)
split.name = 'beat'
del complaints['beat']
split = split.apply(lambda x: x.strip())
complaints = complaints.join(split, how ="right")
complaints['complaint_date'] =  pd.to_datetime(complaints['complaint_date'], format='%Y%m%dT%H:%M:%S.%f')
complaints['complaint_year'] = complaints.complaint_date.dt.year

beats_gpd = gpd.read_file('policebeats.shp')

complaints['complaint_year'].value_counts()
