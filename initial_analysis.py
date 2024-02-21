import pandas as pd
import geopandas as gpd
from shapely import wkt
from shapely.ops import linemerge
import matplotlib.pyplot as plt
import math
from graph import CityNode, TransportNode

def read_excel_to_dataframe(file):
    return pd.read_excel(file)

def read_csv_to_dataframe(file):
    return pd.read_csv(file)

def wkt_loads(x):
    try:
        return wkt.loads(x)
    except Exception:
        return None

def centroid(polygon):
    return polygon.centroid

def speedlimit_grouping(speedlimit_dataframe):
    agg_functions = {
        'time': sum,
    }
    speedlimit_dataframe['road'] = speedlimit_dataframe['vref'].apply(lambda x: x.split("D")[0])
    speedlimit_dataframe['time'] = speedlimit_dataframe.apply(lambda x: (float(x.segmentlengde)/1000)/float(x.Fartsgrense), axis=1)
    speedlimit_dataframe = speedlimit_dataframe[['road', 'time']].groupby('road').agg(agg_functions).reset_index()

    return speedlimit_dataframe

def road_grouping(road_dataframe):
    agg_functions = {
        'geometry': '- '.join,
        'startnode': ', '.join,
        'sluttnode': ', '.join
    }
    road_dataframe['road'] = road_dataframe['vref'].apply(lambda x: x.split("D")[0])
    road_dataframe = road_dataframe[['road','startnode','sluttnode','geometry']].groupby('road').agg(agg_functions).reset_index()
    #print(road_dataframe.shape)

    for index, row in road_dataframe.iterrows():
        value = row['geometry']
        for y in value.split('- '):
            try:
                wkt.loads(y)
            except Exception:
                print(f'{index} [{len(value)}] {y}')
    road_dataframe['noder'] = road_dataframe.apply(lambda x: [i.replace(" ","") for i in x.startnode.split(',') + x.sluttnode.split(',')], axis=1)
    road_dataframe = road_dataframe.drop(columns=['startnode', 'sluttnode'])
    #road_dataframe['noder'] = road_dataframe['startnode'] + ', ' + road_dataframe['sluttnode']
    #road_dataframe['noder'] = road_dataframe['noder'].apply(lambda x: list(set(x.split(', '))))

    road_dataframe['geometry'] = road_dataframe['geometry'].apply(lambda x: linemerge([wkt_loads(y) for y in x.split('- ')]))
    return road_dataframe

def main():
    speedlimit_dataframe = read_csv_to_dataframe("speedlimit.csv")
    speedlimit_dataframe = speedlimit_grouping(speedlimit_dataframe)
    
    road_dataframe = read_csv_to_dataframe("veg.csv")
    road_dataframe = road_grouping(road_dataframe)

    road_gdf = gpd.GeoDataFrame(road_dataframe, geometry='geometry', crs=5973)
    """gdf.plot()
    plt.show()"""

    tettsteder = read_csv_to_dataframe("alle_tettsteder.csv")
    tettsteder['geometry'] = tettsteder['geometry'].apply(lambda x: wkt.loads(x))
    tettsteder_gdf = gpd.GeoDataFrame(tettsteder, geometry='geometry', crs=5973)
    #tettsteder_gdf['centroid'] = tettsteder_gdf['geometry'].apply(lambda x: centroid(x))
    """tettsteder_gdf.plot()
    plt.show()"""

    #road_gdf = road_gdf.overlay(tettsteder_gdf, how='union')
    road_gdf = gpd.sjoin(left_df=road_gdf,right_df=tettsteder_gdf,how='left')
    road_gdf.to_excel("ttttest.xlsx")
    """
    road_gdf['road_centroid'] = road_gdf['geometry'].apply(lambda x: centroid(x))
    road_gdf['color'] = road_gdf['tettstednummer'].apply(lambda x: 'red' if not math.isnan(float(x)) else 'black')
    road_gdf.plot(color=road_gdf['color'])
    plt.show()

    list_of_city_nodes = [CityNode(i.centroid.x, i.centroid.y, i.tettstednummer, i.color, i.totalBefolkning, i.tettstednavn) for i in road_gdf[road_gdf['centroid'].notnull()].itertuples()] 
    list_of_transport_nodes = [TransportNode(i.road_centroid.x, i.road_centroid.y, 1, i.color, 1, 1) for i in road_gdf[road_gdf['centroid'].isnull()].itertuples()]
    #for node in list_of_transport_nodes:
     # node.plotting()
    road_gdf[road_gdf['centroid'].isnull()].plot()
    for node in list_of_city_nodes:
        node.plotting()
    plt.show()"""

main()