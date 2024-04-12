from initial_analysis import read_csv_to_dataframe, wkt_loads
from initial_traffic import traffic_aggregate
from tqdm import tqdm
import pandas as pd
import geopandas as gpd
import json
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr

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

        cityDict[row.tettstednavn.replace('/','&')] = values #tettstednavn: [korrelasjon,befolkning,areal,tetthet,ant.veglenker]
    with open(f"city_data/cityDict.txt", 'w') as fp:
        json.dump(cityDict, fp)
    
    plt.scatter(pop,sorted(cor))
    plt.show()

def city_analysis():
    with open(f"city_data/cityDict.txt", 'r') as fp:
        cityDict = json.load(fp)
    names = []
    corr = []
    pop = []
    area = []
    den = []
    seg = []

    for key, val in cityDict.items():
        names.append(key)
        corr.append(val[0])
        pop.append(val[1])
        area.append(val[2])
        den.append(val[3])
        seg.append(val[4])
    
    plt.scatter(corr, seg)
    plt.xlabel("Correlation")
    plt.ylabel("No of roads")
    print(pearsonr(corr,seg))
    plt.show()

if __name__ == "__main__":
    #main()
    city_analysis()