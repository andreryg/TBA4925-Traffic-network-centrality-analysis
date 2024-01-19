import pandas as pd
import geopandas as gpd
from shapely import wkt
from shapely.ops import linemerge
import matplotlib.pyplot as plt

def read_excel_to_dataframe(file):
    return pd.read_excel(file)

def read_csv_to_dataframe(file):
    return pd.read_csv(file)

def wkt_loads(x):
    try:
        return wkt.loads(x)
    except Exception:
        return None

def road_grouping(road_dataframe):
    agg_functions = {
        'geometry': '- '.join
    }
    road_dataframe['road'] = road_dataframe['vref'].apply(lambda x: x.split("D")[0])
    road_dataframe = road_dataframe[['road', 'geometry']].groupby('road').agg(agg_functions).reset_index()
    print(road_dataframe.shape)

    for index, row in road_dataframe.iterrows():
        value = row['geometry']
        for y in value.split('- '):
            try:
                wkt.loads(y)
            except Exception:
                print(f'{index} [{len(value)}] {y}')

    road_dataframe['geometry'] = road_dataframe['geometry'].apply(lambda x: linemerge([wkt_loads(y) for y in x.split('- ')]))
    return road_dataframe

def main():
    road_dataframe = read_csv_to_dataframe("veg.csv")
    road_dataframe = road_grouping(road_dataframe)

    gdf = gpd.GeoDataFrame(road_dataframe, geometry='geometry', crs=5973)
    gdf.plot()
    plt.show()

main()