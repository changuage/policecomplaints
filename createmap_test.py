import pytest
from createmap import pulldata
import pandas as pd
from App import *



def test_pulldata():
    data = pulldata()
    assert type(data) is pd.core.frame.DataFrame

def test_cleandata():
	data = pulldata()
	cdata = cleandata(data)
    assert type(data) is pd.core.frame.DataFrame
    assert len(data.columns) == 7

def test_create_shapefile():
	shapefile = create_shapefile('App/static/Shapefile/policebeats.shp')
	assert type(data) is geopandas.geodataframe.GeoDataFrame
