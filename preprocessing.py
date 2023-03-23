# Preprocessing functions 

def convertWKT(df, column):
    import geopandas as gpd
    from shapely import wkt
    """
    Converting object columns into WKT format for geoDataFrame for plotting coordinates.
      Parameters
    ----------
    df : DataFrame
    column : string
        column of interest to apply WKT conversion to Polygon coordinates
    Returns
    -------
    DataFrame
        returns the df with converted column to geometry format 
    """
    df[column] = df[column].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df,geometry= column)
    
    return gdf


def percentage_area(df, area1, area2):
    """
    Calculates percentage area of how much of intersection area relative to the plot area of interest, in percent 
      Parameters
    ----------
    df : DataFrame
    area1 : string
        first column of interest to apply 2nd intersection with
    area2: string
        second column to intersect with area1
    Returns
    -------
    Series
        returns series of percentage area in percent 
    """
    return df[area1].intersection(df[area2]).area/df[area1].area*100


def createPlotsPairs(df, title, fig_size = (10, 15), aspect_size= 0.9, intersect_avg_show= True):
    import geopandas as gpd
    import matplotlib.pyplot as plt
    """
    Creates geo graphs for the two Pair plots in one plot for each row in dataframe.
    Parameters
    ----------
    df : DataFrame
    title : string
        title of plot
    fig_size: tuple
        size of figure, default is (10, 15)
    aspect_size: int
        aspect size of plot, default 0.9
    intersect_avg_show: boolean
        prints average intersection percentage when needed, default is True
    Returns
    -------
    matplotlib plot
        returns plots
    """
    for slide in range(len(df)):
        
        if intersect_avg_show is True:
            print('Overlap average percent: {}'.format(round(df['overlap_average_percent'][slide], 3)))
         
        d = {'col1': ['Pair_a', 'Pair_b'], 'geometry': [df.Pair_a[slide], df.Pair_b[slide]]}
        new = gpd.GeoDataFrame(d, crs='EPSG:4326')

        fig, ax = plt.subplots(figsize=fig_size)
        new.plot(column = 'col1', ax=ax, alpha=0.5, aspect=aspect_size, cmap='plasma', legend= True)
        plt.title("{} \nID: {}".format(title, df.id[slide]))
        plt.show()
        
def createPlots(df, column, title, fig_size = (10, 15), aspect_size= 0.9):
    import geopandas as gpd
    import matplotlib.pyplot as plt
    """
    Creates geo graphs for the two Pair plots in one plot for each row in dataframe.
    Parameters
    ----------
    df : DataFrame
    column: string
        column name 
    title : string
        title of plot
    fig_size: tuple
        size of figure, default is (10, 15)
    aspect_size: int
        aspect size of plot, default 0.9
    Returns
    -------
    matplotlib plot
        returns plots
    """
    for slide in range(len(df)):
        d = {'col1': [column], 'geometry': [df[column][slide]]}
        new = gpd.GeoDataFrame(d, crs='EPSG:4326')

        fig, ax = plt.subplots(figsize=fig_size)
        new.plot(column = 'col1', ax=ax, alpha=0.5, aspect=aspect_size, cmap='plasma', legend= True)
        plt.title("{} \nID: {}".format(title, df.id[slide]))
        plt.show()  
    
    