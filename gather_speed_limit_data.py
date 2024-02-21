import nvdbapiv3
import pandas as pd
import geopandas as gpd
from shapely import wkt

def download_speed_limit_data():
    v = nvdbapiv3.nvdbFagdata(105)
    v.filter({'vegsystemreferanse' : ['EV', 'RV']})
    speedlimit_dataframe = pd.DataFrame(v.to_records())

    speedlimit_dataframe['geometry'] = speedlimit_dataframe['geometri'].apply( wkt.loads )
    speedlimit_dataframe.to_csv(f"speedlimit.csv")
    speedlimitGDF = gpd.GeoDataFrame( speedlimit_dataframe, geometry='geometry', crs=5973 )

    return speedlimitGDF

download_speed_limit_data()