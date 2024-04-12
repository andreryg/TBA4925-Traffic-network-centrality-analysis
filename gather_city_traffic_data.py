import nvdbapiv3
import pandas as pd
import geopandas as gpd
from shapely import wkt
from initial_analysis import read_csv_to_dataframe

def download_city_traffic_data(polygon,name):
    v = nvdbapiv3.nvdbFagdata(540)
    v.filter({'polygon' : polygon})
    v.filter({'vegsystemreferanse' : ['EV', 'RV', 'FV', 'KV']})
    road_dataframe = pd.DataFrame(v.to_records())

    typeveg_mask = ((road_dataframe['typeVeg'] == 'Gågate') | (road_dataframe['typeVeg'] == 'Gang- og sykkelveg') | (road_dataframe['typeVeg'] == 'Sykkelveg') | (road_dataframe['typeVeg'] == 'Fortau') | (road_dataframe['typeVeg'] == 'Gangfelt') | (road_dataframe['typeVeg'] == 'Trapp'))
    road_dataframe = road_dataframe[~typeveg_mask]

    detaljnivå_mask = ((road_dataframe['detaljnivå'] == 'Kjørebane') | (road_dataframe['detaljnivå'] == 'Kjørefelt'))
    road_dataframe = road_dataframe[~detaljnivå_mask]

    road_dataframe['geometry'] = road_dataframe['geometri'].apply( wkt.loads )
    road_dataframe.to_csv(f"city_data/traffic_{name}.csv")
    vegGDF = gpd.GeoDataFrame( road_dataframe, geometry='geometry', crs=5973 )

    return vegGDF

def main():
    tettsteder = read_csv_to_dataframe("alle_tettsteder.csv")
    tettsteder['clean_geo'] = tettsteder['geometry'].apply(lambda x: x[10:-2])
    for row in tettsteder.itertuples():
        print(row.tettstednavn)
        download_city_traffic_data(row.clean_geo, row.tettstednavn.replace('/','&'))

if __name__ == "__main__":
    main()