import pandas as pd
import numpy as np
import json
import tqdm
import matplotlib.pyplot as plt

def traffic_aggregate(df):
    agg_functions = {
        'Trafikkmengde': lambda x: [float(i) for i in x],
    }
    df['road'] = df['Vegreferanse'].apply(lambda x: x.split(" m")[0])
    df = df[['road', 'Dato', 'Trafikkmengde']].groupby(['road','Dato']).agg(agg_functions).reset_index()
    df['trafikk'] = df['Trafikkmengde'].apply(lambda x: sum(x)/len(x))

    return df

def main():
    city = "Drammen"
    traffic_df = pd.read_csv(f"city_data/real_time/{city}_day.csv", encoding='ANSI',sep=';')
    traffic_df = traffic_df.dropna(subset=['Trafikkmengde'])
    traffic_df = traffic_df[traffic_df['Trafikkmengde'] != "-"]
    traffic_df = traffic_df[traffic_df['Felt'] == "Totalt"]
    traffic_df = traffic_aggregate(traffic_df)

    with open(f"city_data/centralityDict_{city}.txt", 'r') as fp:
            bc = json.load(fp)
    
    bc_list = [(key, value) for key, value in bc.items()]
    bc_df =  pd.DataFrame(bc_list, columns=['road', 'bc'])

    dates = traffic_df['Dato'].unique()
    correlations = []
    for date in tqdm.tqdm(dates):
        daily_traffic_df = traffic_df[traffic_df['Dato'] == date]
        if len(correlations) == 0:
             print(daily_traffic_df.shape)
        merged_df = pd.merge(daily_traffic_df[['road', 'trafikk']],bc_df, on='road',how='inner')
        correlations.append(merged_df['trafikk'].corr(merged_df['bc']))

    plt.plot(correlations)
    plt.show()
    

if __name__ == "__main__":
    main()