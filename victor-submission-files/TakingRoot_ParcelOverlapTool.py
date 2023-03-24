# Standard Libraries
import pandas as pd
import streamlit as st
import shapely.wkt
import geopandas as gpd
from matplotlib import pyplot as plt

st.set_page_config(
    page_title="Taking Root Parcel Overlap Tool", page_icon="⬇", layout="centered"
)

# get the data, returns a dataframe
@st.cache_data
def get_data(csv):
    data = pd.read_csv(csv)
    return data


# visualize the overlap graph
@st.cache_data()
def get_chart(data, id):
    plot1 = shapely.wkt.loads(data.iloc[id][1])
    plot2 = shapely.wkt.loads(data.iloc[id][2])
    polys = [plot1, plot2]
    colors = ['red', 'blue']
    plotMap = gpd.GeoSeries(polys).boundary.plot(color=colors)
    plt.title("Parcel Overlap")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    st.pyplot(plotMap.figure)

# replace existing parcel value aka 0 is a dupe of 0 so we remove it
def cleanDupeString(string):
    string = string.replace(", " + str(pairID), "")
    string = string.replace(str(pairID) + ", ", "")
    string = string.replace(str(pairID), "")
    return string


st.title("Taking Root - Parcel Overlap Tool")

st.write("Select an ID to view overlaps between parcels!")

max_number = 512
# main logic
try:
    pairID = int(st.text_input("Enter an ID you wish to view", 0))
    if pairID > max_number:
        raise ValueError
    # graph the parcels
    source = get_data('sample-data.csv')
    chart = get_chart(source, int(pairID))

    # display the % overlap
    percentOverlapSortedDF = get_data('percentOverlapSortedDF.csv')
    percentOverlap = percentOverlapSortedDF.loc[(percentOverlapSortedDF["Index"] == pairID)].iloc[0][1]
    st.write("The overlap between these two parcels is: " + str(percentOverlap.round(2)*100) + "%")

    # display the duplicates
    indexStoreDF = get_data('indexStoreDF.csv')
    dupesA = cleanDupeString(indexStoreDF.loc[(indexStoreDF["Index"] == pairID)].iloc[0][1])
    dupesB = cleanDupeString(indexStoreDF.loc[(indexStoreDF["Index"] == pairID)].iloc[0][2])

    st.write("Parcel A Duplicates: " + str(dupesA))
    st.write("Parcel B Duplicates: " + str(dupesB))

except ValueError:
    st.write("That ID doesn't exist, choose another one!")
