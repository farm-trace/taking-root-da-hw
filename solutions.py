#import packages 

import pandas as pd
from shapely.geometry import Polygon, MultiPolygon
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely import wkt, geometry
from matplotlib import pyplot
import numpy as np
from preprocessing import convertWKT, percentage_area, createPlots
import scipy as sp
import plotly.express as px

#reading in data 
data = pd.read_csv("data/sample-data.csv")
df= data.copy()

#convert data type into geometry type
gdf = convertWKT(df, 'Pair_a')
gdf = convertWKT(df, 'Pair_b')

# new column for intersection of the two plots, like an inner join of polygon shapes
gdf['intersect_plots'] = gdf['Pair_a'].intersection(gdf['Pair_b'])

# new column for difference of the two plots, like an outer join of polygon shapes
# Ones with POLYGON EMPTY will be flagged for project managers to address issue 
gdf['difference'] = gdf['Pair_a'].difference(gdf['Pair_b'])

# percentage of area of overlap for plot a and plot b
gdf['overlap_area_plota_percent'] = percentage_area(gdf, 'Pair_a', 'Pair_b')
gdf['overlap_area_plotb_percent'] = percentage_area(gdf, 'Pair_b', 'Pair_a')
# average of percentages
gdf['overlap_average_percent'] = (gdf['overlap_area_plota_percent']+ gdf['overlap_area_plotb_percent'])/2

#setting threshold metrics for different overlaps 
union_overlaps = gdf.query('overlap_average_percent <= 5').reset_index(drop= True)
needs_review_overlaps = gdf.query('5 < overlap_average_percent & overlap_average_percent <= 95').reset_index(drop= True)
full_overlaps = gdf.query('overlap_average_percent > 95').reset_index(drop= True)

# Union 
union_overlaps['union'] = union_overlaps['Pair_a'].union(union_overlaps['Pair_b'])

#saving full overlaps 
full_overlaps_df = full_overlaps[['id', 'Pair_a', 'Pair_b', 'intersect_plots', 'overlap_average_percent']]
full_overlaps_df.to_csv('outputs/full_overlaps_df.csv', index= False)
