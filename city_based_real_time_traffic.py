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
    city = "Lillehammer"
    traffic_df = pd.read_csv(f"city_data/real_time/{city}_day.csv", encoding='ANSI',sep=';')
    traffic_df = traffic_df.dropna(subset=['Trafikkmengde'])
    traffic_df = traffic_df[traffic_df['Trafikkmengde'] != "-"]
    traffic_df = traffic_df[traffic_df['Felt'] == "Totalt"]
    traffic_df_agg = traffic_aggregate(traffic_df)

    with open(f"city_data/centralityDict_{city}.txt", 'r') as fp:
            bc = json.load(fp)
    
    bc_list = [(key, value) for key, value in bc.items()]
    bc_df =  pd.DataFrame(bc_list, columns=['road', 'bc'])

    dates = traffic_df_agg['Dato'].unique()
    correlations = []
    traffic = []
    counters = traffic_df['Trafikkregistreringspunkt'].unique()
    for date in tqdm.tqdm(dates):
        daily_traffic_df = traffic_df_agg[traffic_df_agg['Dato'] == date]
        if len(correlations) == 0:
             print(daily_traffic_df.shape)
        merged_df = pd.merge(daily_traffic_df[['road', 'trafikk']],bc_df, on='road',how='inner')
        correlations.append(merged_df['trafikk'].corr(merged_df['bc']))
        traffic.append(sum(daily_traffic_df['trafikk'].values.tolist())/len(daily_traffic_df['trafikk'].values.tolist()))

    plt.subplot(2,1,1)
    for counter in counters:
        counter_list = [] 
        counter_df = traffic_df[traffic_df['Trafikkregistreringspunkt'] == counter]
        counter_dates = counter_df['Dato'].unique()
        for date in dates:
            if date in counter_dates:
                counter_list.append(float(counter_df[counter_df['Dato'] == date]['Trafikkmengde'].values.tolist()[0]))
            else:
                counter_list.append(np.nan)
        plt.plot(counter_list)

    traffic = [i / max(traffic) for i in traffic]
    #plt.plot(traffic)
    plt.subplot(2,1,2)
    plt.plot(correlations)
    plt.show()
    

if __name__ == "__main__":
    main()