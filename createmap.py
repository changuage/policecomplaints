import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sodapy import Socrata
from geopandas import gpd
import pysal as ps
import numpy as np
import folium

from App import db
from App.models import beatcomplaint


def pulldata():

	"""Pulls and returns police complaint data from the api""" 
	client = Socrata("data.cityofchicago.org", 'EjrjYzG6YAkBx7bPBzME8jD4c')
	results = client.get("w3hi-cfa4",limit = 500000)
	data = pd.DataFrame.from_records(results)

	return data

def cleandata(data):
	"""Cleans initial police data""" 
	split = data['beat'].str.split('|').apply(pd.Series, 1).stack()
	split.index = split.index.droplevel(-1)
	split.name = 'beat'
	del data['beat']
	split = split.apply(lambda x: x.strip())
	data = data.join(split, how ="right")
	data['complaint_date'] =  pd.to_datetime(data['complaint_date'], format='%Y%m%dT%H:%M:%S.%f')
	data['complaint_year'] = data.complaint_date.dt.year
	data = data.drop(['age_of_complainant','assignment','case_type','complaint_month','complaint_day','complaint_hour',
                'current_status','finding_code','police_shooting','sex_of_complainant'],axis=1)
	return data

def create_shapefile(fileloc):
	"""Reads the shapefile at the filelocation (fileloc)"""
	shapefile = gpd.read_file(fileloc)
	shapefile['beat_num'] = pd.to_numeric(shapefile['beat_num'])

	return shapefile

def add_race(shapefile, data):
	"""Appends aggregated race tabulations of police complaints to a beats-level dataframe"""
	race = data[['beat','race_of_complainant']].dropna()
	race_long = pd.get_dummies(race, columns = ['race_of_complainant']) 
	race_long.rename(columns={'race_of_complainant_African American / Black':'Black', 
	                          'race_of_complainant_American Indian or Alaskan Native':'AmerIndianAlaskan',
	                         'race_of_complainant_Asian or Pacific Islander':'Apia',
	                          'race_of_complainant_Hispanic':'Hispanic',
	                          'race_of_complainant_Unknown':'Unknown',
	                          'race_of_complainant_White':'White'
	                         }, inplace=True)
	race_long =race_long.groupby(['beat']).agg({'Black':[sum],'AmerIndianAlaskan':[sum],
	                                'Apia':[sum],'Hispanic':[sum],
	                                'Unknown':[sum],'White':[sum]})
	race_long.columns = race_long.columns.droplevel(1)
	race_long = race_long.reset_index()
	race_long['beat'] = pd.to_numeric(race_long['beat'])


	shapefile = shapefile.merge(race_long,right_on='beat',left_on='beat_num', how ='left')
	shapefile = shapefile.fillna(0)

	return shapefile

def add_type(shapefile, data):
	"""Appends aggregated complaint type tabulations of police complaints to a beats-level dataframe"""
	typeaction = data[['beat','current_category']].dropna()
	type_long = pd.get_dummies(typeaction, columns=['current_category'])
	type_long = type_long.rename(columns={'current_category_Bias':'bias',
	                         'current_category_Civil Suits':'civilsuits',
	                         'current_category_Coercion':'coercion',
	                         'current_category_Death or Injury In Custody':'deathinjuryincustody',
	                         'current_category_Domestic Violence':'domesticviolence',
	                         'current_category_Excessive Force':'excessforce',
	                         'current_category_Firearm Discharge - Hits':'firearmhit',
	                         'current_category_Firearm Discharge - No Hits':'firearmnohit',
	                         'current_category_Firearm Discharge at Animal':'firearmanimal',
	                         'current_category_Legal Violation':'legalviol',
	                         'current_category_Miscellaneous':'misc',
	                         'current_category_Motor Vehicle Related Death':'motordeath',
	                         'current_category_OC Discharge':'ocdischarge',
	                         'current_category_Operational Violation':'operationviolation',
	                         'current_category_Search or Seizure':'searchseizure',
	                         'current_category_Taser Discharge':'taserdischarge',
	                         'current_category_Taser Notification':'tasernotif',
	                         'current_category_Unlawful Denial of Counsel':'denialcounsel',
	                         'current_category_Unnecessary Display of Weapon':'unnecessarydispweapon',
	                         'current_category_Verbal Abuse':'verbalabuse'})
	type_long = type_long.groupby(['beat']).agg({'bias':[sum],'civilsuits':[sum],
	                                'coercion':[sum],'deathinjuryincustody':[sum],
	                                'domesticviolence':[sum],'excessforce':[sum],
	                               'firearmhit':[sum],'firearmnohit':[sum],
	                                'firearmanimal':[sum],'legalviol':[sum],
	                                'misc':[sum],'motordeath':[sum],
	                               'ocdischarge':[sum],'operationviolation':[sum],
	                                'searchseizure':[sum],'taserdischarge':[sum],
	                                'tasernotif':[sum],'denialcounsel':[sum],
	                               'unnecessarydispweapon':[sum],'verbalabuse':[sum]})
	type_long.columns = type_long.columns.droplevel(1)
	type_long = type_long.reset_index()
	type_long['beat'] = pd.to_numeric(type_long['beat'])

	shapefile = shapefile.merge(type_long,right_on='beat',left_on='beat_num', how ='left')
	shapefile = shapefile.fillna(0)

	return shapefile


def spatialcorrelation(data,column,filename):
	"""Performs a spatial correlation on the column and exports an html map of hot/cold spots"""
	W = ps.weights.Queen.from_dataframe(data)
	W.transform = 'r'
	moran = ps.Moran_Local(column.values, W, permutations=9999)
	sig = moran.p_sim < 0.05
	hotspots = moran.q==1 * sig
	coldspots = moran.q==3 * sig
	hotcold = hotspots*1 + coldspots*2
	if filename=='blank':
		hotcold = hotspots*0
	hc_df = pd.DataFrame(hotcold)

	mapdata = data.join(hc_df)
	mapdata.rename(columns={0: 'type'}, inplace=True)

	style = pd.DataFrame({'type': [0,1,2], 'style': [
	    {'fillColor': '#e3dfd6', 'weight': .15, 'color': 'black'},
	    {'fillColor': '#dd3232', 'fillOpacity' : .55, 'weight': .25, 'color': 'black'},
	    {'fillColor': '#a2d0cf', 'fillOpacity' : .55, 'weight': .25, 'color': 'black'},
	    ]})
	mapdata = mapdata.merge(style)

	cook_coords = [41.857602, -87.731696]
	width, height = 400, 500

	my_map = folium.Map(location = cook_coords, zoom_start = 10, 
	                    tiles = 'cartodbpositron')

	folium.GeoJson(mapdata.to_crs({'init': 'epsg:4326'}).to_json()).add_to(my_map)

	my_map.save('App/static/Maps/'+filename +'.html')

def backuptords(data):
	
	#Deletes previous data
	db.session.query(beatcomplaint).delete()
	
	#Writes new data to RDS
	for index, row in data.iterrows():
   		complaint = beatcomplaint(id = index, 
   			beat=str(row[0]), 
   			complaint_date=str(row[1]), 
   			current_category=str(row[2]),
   			log_no=str(row[3]),
   			race_of_complainant=str(row[4]))
   		db.session.add(complaint)
	db.session.commit()

if __name__ == "__main__":
	#Pulls data from API
	complaint = pulldata()
	complaint = cleandata(complaint)
	#backuptords(complaint)

	#Reads the police beats shapefile
	beats = create_shapefile('App/static/Shapefile/policebeats.shp')
	
	#Appends race tabulations to the beats shapefile and creates maps
	beats_race = add_race(beats, complaint)

	spatialcorrelation(beats_race, beats_race.Black, 'black')
	spatialcorrelation(beats_race, beats_race.White, 'white')
	spatialcorrelation(beats_race, beats_race.AmerIndianAlaskan, 'amerindian')
	spatialcorrelation(beats_race, beats_race.Apia, 'apia')
	spatialcorrelation(beats_race, beats_race.Hispanic, 'hispanic')
	spatialcorrelation(beats_race, beats_race.Unknown, 'unknown')

	#appends complaint type tabulations to the beats shapefile and creates maps
	beats_type = add_type(beats, complaint)

	spatialcorrelation(beats_type, beats_type.firearmhit, 'firearmhit')
	spatialcorrelation(beats_type, beats_type.excessforce, 'excessforce')
	spatialcorrelation(beats_type, beats_type.firearmanimal, 'firearmanimal')
	spatialcorrelation(beats_type, beats_type.coercion, 'coercion')
	spatialcorrelation(beats_type, beats_type.deathinjuryincustody, 'deathinjuryincustody')

	spatialcorrelation(beats_race, beats_race.Black, 'blank')
