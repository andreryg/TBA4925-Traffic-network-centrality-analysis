from city_based_real_time_traffic import traffic_aggregate
import pandas as pd
import json
import tqdm
import matplotlib.pyplot as plt
import numpy as np

def main():
    df1 = pd.read_csv("daily_traffic_1.csv", encoding='ANSI',sep=';')
    df2 = pd.read_csv("daily_traffic_2.csv", encoding='ANSI',sep=';')
    df3 = pd.read_csv("daily_traffic_3.csv", encoding='ANSI',sep=';')
    df4 = pd.read_csv("daily_traffic_4.csv", encoding='ANSI',sep=';')
    df5 = pd.read_csv("daily_traffic_5.csv", encoding='ANSI',sep=';')
    df6 = pd.read_csv("daily_traffic_6.csv", encoding='ANSI',sep=';')
    df7 = pd.read_csv("daily_traffic_7.csv", encoding='ANSI',sep=';')
    df8 = pd.read_csv("daily_traffic_8.csv", encoding='ANSI',sep=';')
    dfs = [df1, df2, df3, df4, df5, df6, df7, df8]

    traffic_df = pd.concat(dfs)
    traffic_df = traffic_df.dropna(subset=['Trafikkmengde'])
    traffic_df = traffic_df[traffic_df['Trafikkmengde'] != "-"]
    traffic_df = traffic_df[traffic_df['Felt'] == "Totalt"]
    traffic_df_agg = traffic_aggregate(traffic_df)
    print(traffic_df_agg.shape)

    with open(f"centralityDict.txt", 'r') as fp:
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
    for counter in tqdm.tqdm(counters):
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