from initial_analysis import read_csv_to_dataframe, wkt_loads
from initial_traffic import traffic_aggregate
from tqdm import tqdm
import pandas as pd
import geopandas as gpd
import json
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import shapely

def main():
    tettsteder = read_csv_to_dataframe("alle_tettsteder.csv")
    pop = []
    cor = []
    cityDict = {}
    for row in tqdm(tettsteder.itertuples(), total=tettsteder.shape[0]):
        values = []
        traffic_df = read_csv_to_dataframe(f"city_data/traffic_{row.tettstednavn.replace('/','&')}.csv")
        traffic_df = traffic_aggregate(traffic_df)

        with open(f"city_data/centralityDict_{row.tettstednavn.replace('/','&')}.txt", 'r') as fp:
            bc = json.load(fp)
    
        bc_list = [(key, value) for key, value in bc.items()]
        bc_df =  pd.DataFrame(bc_list, columns=['road', 'bc'])

        merged_df = pd.merge(traffic_df[['road', 'average_ådt']],bc_df, on='road',how='inner')
        corr = merged_df['average_ådt'].corr(merged_df['bc'])
        cor.append(corr)
        pop.append(row.Index)#int(row.totalBefolkning))

        values.append(corr)
        values.append(int(row.totalBefolkning))
        values.append(wkt_loads(row.geometry).area)
        values.append(values[1]/values[2])
        values.append(bc_df.shape[0])
        values.append(str(shapely.centroid(wkt_loads(row.geometry))))
        values.append(len([v for v in bc_df['road'].values.tolist() if "EV" in v])/bc_df.shape[0])
        values.append(len([v for v in bc_df['road'].values.tolist() if "RV" in v])/bc_df.shape[0])
        values.append(len([v for v in bc_df['road'].values.tolist() if "FV" in v])/bc_df.shape[0])
        values.append(len([v for v in bc_df['road'].values.tolist() if "KV" in v])/bc_df.shape[0])

        cityDict[row.tettstednavn.replace('/','&')] = values #tettstednavn: [korrelasjon,befolkning,areal,tetthet,ant.veglenker]
    with open(f"city_data/cityDict.txt", 'w') as fp:
        json.dump(cityDict, fp)
    
    plt.scatter(pop,sorted(cor))
    plt.show()

def city_analysis():
    with open(f"city_data/cityDict.txt", 'r') as fp:
        cityDict = json.load(fp)
    #del cityDict['Oslo']
    cities = []

    for key, val in cityDict.items():
        cities.append([key, val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7], val[8], val[9]])
    
    cities = pd.DataFrame(cities,columns=['Names', 'Correlation', 'Population', 'Area', 'Density', 'Segments', 'Centroid','EV_ratio','RV_ratio','FV_ratio','KV_ratio'])
    cities['Centroid'] = cities['Centroid'].apply(lambda x: wkt_loads(x))
    citiesGDF = gpd.GeoDataFrame(cities, geometry='Centroid', crs=5973)
    colors = ['#edf8fb', '#b3cde3', '#8c96c6', '#8856a7', '#252525']
    """citiesGDF['color'] = citiesGDF['Correlation'].apply(lambda x: colors[0] if x<0 else colors[1] if x<0.25 else colors[2] if x<0.50 else colors[3] if x<0.75 else colors[4])
    citiesGDF.plot(color=citiesGDF['color'])
    plt.show()"""

    #citiesGDF.to_excel("city_analysis.xlsx")

    plt.scatter(cities['Correlation'], cities['Segments'])
    plt.xlabel("Correlation")
    plt.ylabel("No of roads")
    print(pearsonr(cities['Correlation'],cities['Segments']))
    plt.show()

if __name__ == "__main__":
    #main()
    city_analysis()