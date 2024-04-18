import pandas as pd
import geopandas as gpd
from shapely import wkt, Polygon, MultiPoint
import numpy as np
import matplotlib.pyplot as plt

tettsteder = pd.read_csv("tettsteder_xml_file.csv")

#tettsteder = tettsteder[tettsteder['tettstednavn'] == "Oslo"]
#tettsteder['geometry'] = tettsteder['posList'].apply(lambda x: Polygon(x))

#print(sorted(tettsteder['tettstednavn'].tolist()))
def convex_hull(string):
    lst = string.split()

    d2_lst = []
    for i,v in enumerate(lst):
        if i%2 != 0 and i != 0:
            d2_lst.append([float(lst[i-1]), float(lst[i])])
    multipnt = MultiPoint(d2_lst)
    hull = multipnt.convex_hull.wkt

    """ """

    return hull

def aggregate(dataframe):
    agg_functions = {
        'posList': " ".join,
        'totalBefolkning': max,
        'tettstednavn': max
    }

    dataframe = dataframe[['tettstednavn','posList','totalBefolkning','tettstednummer']].groupby('tettstednummer').agg(agg_functions).reset_index()

    dataframe["geometry"] = dataframe["posList"].apply(lambda x: wkt.loads(convex_hull(x)))

    return dataframe

tettsteder = aggregate(tettsteder)
tettsteder = tettsteder[tettsteder['totalBefolkning'].apply(lambda x: int(x)) > 10000]

tettsteder_2 = pd.read_excel("tettsteder.xlsx")
#print(tettsteder_2.columns.values.tolist())
#print(tettsteder.columns.values.tolist())

tettsteder_2 = tettsteder_2.merge(tettsteder[['tettstednavn','totalBefolkning','tettstednummer','geometry']], on="tettstednavn", how='inner')

gdf = gpd.GeoDataFrame(tettsteder_2, geometry='geometry', crs=5973)
gdf.plot()
plt.show()

"""with open('test.txt', 'w') as f:
    f.write(str(tettsteder["convex_hull"][0]))"""

#tettsteder_2.to_csv("alle_tettsteder.csv")
#tettsteder[['tettstednavn','totalBefolkning','tettstednummer','geometry']].to_csv("convex_hulls.csv")