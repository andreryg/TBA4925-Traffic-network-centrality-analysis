import nvdbapiv3
import pandas as pd
import geopandas as gpd
from shapely import wkt

def download_road_data():
    v = nvdbapiv3.nvdbVegnett()
    v.filter({'vegsystemreferanse' : ['EV', 'RV']})
    road_dataframe = pd.DataFrame(v.to_records())

    typeveg_mask = ((road_dataframe['typeVeg'] == 'Gågate') | (road_dataframe['typeVeg'] == 'Gang- og sykkelveg') | (road_dataframe['typeVeg'] == 'Sykkelveg') | (road_dataframe['typeVeg'] == 'Fortau') | (road_dataframe['typeVeg'] == 'Gangfelt') | (road_dataframe['typeVeg'] == 'Trapp'))
    road_dataframe = road_dataframe[~typeveg_mask]

    detaljnivå_mask = ((road_dataframe['detaljnivå'] == 'Kjørebane') | (road_dataframe['detaljnivå'] == 'Kjørefelt'))
    road_dataframe = road_dataframe[~detaljnivå_mask]

    road_dataframe['geometry'] = road_dataframe['geometri'].apply( wkt.loads )
    road_dataframe.to_csv(f"veg.csv")
    vegGDF = gpd.GeoDataFrame( road_dataframe, geometry='geometry', crs=5973 )

    return vegGDF

download_road_data()
