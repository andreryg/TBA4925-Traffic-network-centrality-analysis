import pandas as pd
import geopandas as gpd
from shapely import wkt
from shapely.ops import linemerge
import matplotlib.pyplot as plt
import math
from graph import CityNode, TransportNode
import nvdbapiv3
import json
import networkx as nx
import re

def download_traffic():
    t = nvdbapiv3.nvdbFagdata(540)
    t.filter({'vegsystemreferanse' : ['EV', 'RV']})
    traffic = pd.DataFrame(t.to_records())
    traffic['geometry'] = traffic['geometri'].apply( wkt.loads )
    traffic.to_excel(f"traffic-mainroads.xlsx")

def download_feltoversikt():
    t = nvdbapiv3.nvdbFagdata(616)
    t.filter({'vegsystemreferanse' : ['EV', 'RV']})
    feltoversik = pd.DataFrame(t.to_records())
    feltoversik['geometry'] = feltoversik['geometri'].apply( wkt.loads )
    feltoversik.to_excel(f"feltoversikt-mainroads.xlsx")

def download_bomstasjon():
    t = nvdbapiv3.nvdbFagdata(45)
    t.filter({'vegsystemreferanse' : ['EV', 'RV']})
    bomstasjon = pd.DataFrame(t.to_records())
    bomstasjon['geometry'] = bomstasjon['geometri'].apply( wkt.loads )
    bomstasjon.to_excel(f"bomstasjon-mainroads.xlsx")

def download_vertikalelement():
    t = nvdbapiv3.nvdbFagdata(640)
    t.filter({'vegsystemreferanse' : ['EV', 'RV']})
    vertikalelement = pd.DataFrame(t.to_records())
    vertikalelement['geometry'] = vertikalelement['geometri'].apply( wkt.loads )
    vertikalelement.to_excel(f"vertikalelement-mainroads.xlsx")

def download_horisontalelement():
    t = nvdbapiv3.nvdbFagdata(639)
    t.filter({'vegsystemreferanse' : ['EV', 'RV']})
    horisontalelement = pd.DataFrame(t.to_records())
    horisontalelement['geometry'] = horisontalelement['geometri'].apply( wkt.loads )
    horisontalelement.to_excel(f"horisontalelement-mainroads.xlsx")

def download_midtdeler():
    t = nvdbapiv3.nvdbFagdata(5)
    t.filter({'vegsystemreferanse' : ['EV', 'RV'],'egenskap' : '1248=11789 OR 1248=11788'})
    midtdeler = pd.DataFrame(t.to_records())
    midtdeler['geometry'] = midtdeler['geometri'].apply( wkt.loads )
    midtdeler.to_excel(f"midtdeler-mainroads.xlsx")

def download_stigning():
    t = nvdbapiv3.nvdbFagdata(825)
    t.filter({'vegsystemreferanse' : ['EV', 'RV']})
    stigning = pd.DataFrame(t.to_records())
    stigning['geometry'] = stigning['geometri'].apply( wkt.loads )
    stigning.to_excel(f"stigning-mainroads.xlsx")

def download_vegkryss():
    t = nvdbapiv3.nvdbFagdata(37)
    t.filter({'vegsystemreferanse' : ['EV', 'RV']})
    vegkryss = pd.DataFrame(t.to_records())
    vegkryss['geometry'] = vegkryss['geometri'].apply( wkt.loads )
    vegkryss.to_excel(f"vegkryss-mainroads.xlsx")

def download_motorveg():
    t = nvdbapiv3.nvdbFagdata(595)
    t.filter({'vegsystemreferanse' : ['EV', 'RV']})
    motorveg = pd.DataFrame(t.to_records())
    motorveg['geometry'] = motorveg['geometri'].apply( wkt.loads )
    motorveg.to_excel(f"motorveg-mainroads.xlsx")

def download_vegbredde():
    t = nvdbapiv3.nvdbFagdata(838)
    t.filter({'vegsystemreferanse' : ['EV', 'RV']})
    vegbredde = pd.DataFrame(t.to_records())
    vegbredde['geometry'] = vegbredde['geometri'].apply( wkt.loads )
    vegbredde.to_excel(f"vegbredde-mainroads.xlsx")

def download_fartsdemper():
    t = nvdbapiv3.nvdbFagdata(103)
    t.filter({'vegsystemreferanse' : ['EV', 'RV']})
    fartsdemper = pd.DataFrame(t.to_records())
    fartsdemper['geometry'] = fartsdemper['geometri'].apply( wkt.loads )
    fartsdemper.to_excel(f"fartsdemper-mainroads.xlsx")

def download_forkjørsveg():
    t = nvdbapiv3.nvdbFagdata(596)
    t.filter({'vegsystemreferanse' : ['EV', 'RV']})
    forkjørsveg = pd.DataFrame(t.to_records())
    forkjørsveg['geometry'] = forkjørsveg['geometri'].apply( wkt.loads )
    forkjørsveg.to_excel(f"forkjørsveg-mainroads.xlsx")

def download_rasteplass():
    t = nvdbapiv3.nvdbFagdata(39)
    t.filter({'vegsystemreferanse' : ['EV', 'RV']})
    rasteplass = pd.DataFrame(t.to_records())
    rasteplass['geometry'] = rasteplass['geometri'].apply( wkt.loads )
    rasteplass.to_excel(f"rasteplass-mainroads.xlsx")

def download_rekkverk():
    t = nvdbapiv3.nvdbFagdata(5)
    t.filter({'vegsystemreferanse' : ['EV', 'RV']})
    rekkverk = pd.DataFrame(t.to_records())
    rekkverk['geometry'] = rekkverk['geometri'].apply( wkt.loads )
    rekkverk.to_excel(f"rekkverk-mainroads.xlsx")

def download_skiltpunkt():
    t = nvdbapiv3.nvdbFagdata(95)
    t.filter({'vegsystemreferanse' : ['EV', 'RV']})
    skiltpunkt = pd.DataFrame(t.to_records())
    skiltpunkt['geometry'] = skiltpunkt['geometri'].apply( wkt.loads )
    skiltpunkt.to_excel(f"skiltpunkt-mainroads.xlsx")

def download_fartsgrense():
    t = nvdbapiv3.nvdbFagdata(105)
    t.filter({'vegsystemreferanse' : ['EV', 'RV']})
    fartsgrense = pd.DataFrame(t.to_records())
    fartsgrense['geometry'] = fartsgrense['geometri'].apply( wkt.loads )
    fartsgrense.to_excel(f"fartsgrense-mainroads.xlsx")

def download_tunnel():
    t = nvdbapiv3.nvdbFagdata(581)
    t.filter({'vegsystemreferanse' : ['EV', 'RV']})
    tunnel = pd.DataFrame(t.to_records())
    tunnel['geometry'] = tunnel['geometri'].apply( wkt.loads )
    tunnel.to_excel(f"tunnel-mainroads.xlsx")

def download_skjerm():
    t = nvdbapiv3.nvdbFagdata(3)
    t.filter({'vegsystemreferanse' : ['EV', 'RV']})
    skjerm = pd.DataFrame(t.to_records())
    skjerm['geometry'] = skjerm['geometri'].apply( wkt.loads )
    skjerm.to_excel(f"skjerm-mainroads.xlsx")

def traffic_aggregate(df):
    agg_functions = {
        'ÅDT, total': lambda col: col.tolist(),
        'segmentlengde': lambda cal: cal.tolist()
    }
    df['road'] = df['vref'].apply(lambda x: x.split(" m")[0])
    df = df[['road','ÅDT, total','segmentlengde']].groupby('road').agg(agg_functions).reset_index()

    df = df.rename(columns={'ÅDT, total': 'ådt'})
    df['average_ådt'] = df.apply(lambda x: sum([y * z for y,z in zip(x.ådt,x.segmentlengde)])/sum(x.segmentlengde),axis=1)

    return df

def feltoversikt_aggregate(df):
    agg_functions = {
        'felt': lambda col: col.tolist(),
        'segmentlengde': lambda cal: cal.tolist()
    }
    df['road'] = df['vref'].apply(lambda x: x.split("D")[0])
    df = df[df['trafikantgruppe'] == 'K']
    df['felt'] = df['Feltoversikt i veglenkeretning'].apply(lambda x: max([int(match) for match in re.findall(r'\d+', x)]))
    df = df[['road','felt','segmentlengde']].groupby('road').agg(agg_functions).reset_index()

    df['average_felt'] = df.apply(lambda x: sum([y * z for y,z in zip(x.felt,x.segmentlengde)])/sum(x.segmentlengde),axis=1)

    return df

def bomstasjon_aggregate(df):
    agg_functions = {
        'Takst liten bil': lambda col: col.tolist()
    }
    df['road'] = df['vref'].apply(lambda x: x.split("D")[0])
    df = df[['road','Takst liten bil']].groupby('road').agg(agg_functions).reset_index()

    df['total_takst'] = df['Takst liten bil'].apply(lambda x: sum(x))

    return df

def vertikalelement_aggregate(df):
    agg_functions = {
        'Stigning, start': lambda col: col.tolist(),
        'segmentlengde': lambda cal: cal.tolist()
    }
    df['road'] = df['vref'].apply(lambda x: x.split("D")[0])
    df = df[df['trafikantgruppe'] == 'K']
    df = df[['road','Stigning, start','segmentlengde']].groupby('road').agg(agg_functions).reset_index()

    df = df.rename(columns={'Stigning, start': 'stigning'})
    df['average_stigning'] = df.apply(lambda x: sum([abs(y) * abs(z) for y,z in zip(x.stigning,x.segmentlengde)])/sum(x.segmentlengde),axis=1)

    return df

def horisontalelement_aggregate(df):
    agg_functions = {
        'Radius': lambda col: col.tolist(),
        'segmentlengde': lambda cal: cal.tolist()
    }
    df['road'] = df['vref'].apply(lambda x: x.split("D")[0])
    df = df[df['trafikantgruppe'] == 'K']
    df = df[df['Radius'] != 99999]
    df = df[['road','Radius','segmentlengde']].groupby('road').agg(agg_functions).reset_index()
    
    df['average_radius'] = df.apply(lambda x: sum([abs(y) * abs(z) for y,z in zip(x.Radius,x.segmentlengde)])/sum(x.segmentlengde),axis=1)
    df = df[df['average_radius'] < 3001]

    return df

def midtdeler_aggregate(df):
    agg_functions = {
        'segmentlengde': sum
    }
    df['road'] = df['vref'].apply(lambda x: x.split("D")[0])
    df = df[['road','segmentlengde']].groupby('road').agg(agg_functions).reset_index()
    df = df.rename(columns={'segmentlengde': 'lengde'})

    return df

def stigning_aggregate(df):
    agg_functions = {
        'Stigning': lambda col: col.tolist(),
        'segmentlengde': lambda cal: cal.tolist()
    }
    df['road'] = df['vref'].apply(lambda x: x.split("D")[0])
    df = df[df['trafikantgruppe'] == 'K']
    df = df[['road','Stigning','segmentlengde']].groupby('road').agg(agg_functions).reset_index()

    df['average_stigning'] = df.apply(lambda x: sum([abs(y) * abs(z) for y,z in zip(x.Stigning,x.segmentlengde)])/sum(x.segmentlengde),axis=1)

    return df

def vegkryss_aggregate(df):
    agg_functions = {
        'versjon': lambda col: col.tolist()
    }
    df['road'] = df['vref'].apply(lambda x: x.split("D")[0])
    df = df[['road','versjon']].groupby('road').agg(agg_functions).reset_index()

    df['number_of_vegkryss'] = df['versjon'].apply(lambda x: len(x))

    return df

def motorveg_aggregate(df):
    agg_functions = {
        'segmentlengde': sum
    }
    df['road'] = df['vref'].apply(lambda x: x.split("D")[0])
    df = df[['road','segmentlengde']].groupby('road').agg(agg_functions).reset_index()
    df = df.rename(columns={'segmentlengde': 'lengde'})

    return df

def vegbredde_aggregate(df):
    agg_functions = {
        'Dekkebredde': lambda col: col.tolist(),
        'segmentlengde': lambda cal: cal.tolist()
    }
    df['road'] = df['vref'].apply(lambda x: x.split("D")[0])
    df = df[df['trafikantgruppe'] == 'K']
    df = df[['road','Dekkebredde','segmentlengde']].groupby('road').agg(agg_functions).reset_index()

    df['average_dekkebredde'] = df.apply(lambda x: sum([abs(y) * abs(z) for y,z in zip(x.Dekkebredde,x.segmentlengde)])/sum(x.segmentlengde),axis=1)

    return df

def fartsdemper_aggregate(df):
    agg_functions = {
        'versjon': lambda col: col.tolist()
    }
    df['road'] = df['vref'].apply(lambda x: x.split("D")[0])
    df = df[['road','versjon']].groupby('road').agg(agg_functions).reset_index()

    df['number_of_fartsdemper'] = df['versjon'].apply(lambda x: len(x))

    return df

def forkjørsveg_aggregate(df):
    agg_functions = {
        'segmentlengde': sum
    }
    df['road'] = df['vref'].apply(lambda x: x.split("D")[0])
    df = df[['road','segmentlengde']].groupby('road').agg(agg_functions).reset_index()
    df = df.rename(columns={'segmentlengde': 'lengde'})

    return df

def rasteplass_aggregate(df):
    agg_functions = {
        'versjon': lambda col: col.tolist()
    }
    df['road'] = df['vref'].apply(lambda x: x.split("D")[0])
    df = df[['road','versjon']].groupby('road').agg(agg_functions).reset_index()

    df['number_of_rasteplass'] = df['versjon'].apply(lambda x: len(x))

    return df

def rekkverk_aggregate(df):
    agg_functions = {
        'segmentlengde': sum
    }
    df['road'] = df['vref'].apply(lambda x: x.split("D")[0])
    df = df[['road','segmentlengde']].groupby('road').agg(agg_functions).reset_index()
    df = df.rename(columns={'segmentlengde': 'lengde'})

    return df

def skiltpunkt_aggregate(df):
    agg_functions = {
        'versjon': lambda col: col.tolist()
    }
    df['road'] = df['vref'].apply(lambda x: x.split("D")[0])
    df = df[['road','versjon']].groupby('road').agg(agg_functions).reset_index()

    df['number_of_skiltpunkt'] = df['versjon'].apply(lambda x: len(x))

    return df

def fartsgrense_aggregate(df):
    agg_functions = {
        'Fartsgrense': lambda col: col.tolist(),
        'segmentlengde': lambda cal: cal.tolist()
    }
    df['road'] = df['vref'].apply(lambda x: x.split("D")[0])
    df = df[df['trafikantgruppe'] == 'K']
    df = df[['road','Fartsgrense','segmentlengde']].groupby('road').agg(agg_functions).reset_index()

    df['average_fartsgrense'] = df.apply(lambda x: sum([abs(y) * abs(z) for y,z in zip(x.Fartsgrense,x.segmentlengde)])/sum(x.segmentlengde),axis=1)

    return df

def tunnel_aggregate(df):
    agg_functions = {
        'versjon': lambda col: col.tolist()
    }
    df['road'] = df['vref'].apply(lambda x: x.split("D")[0])
    df = df[['road','versjon']].groupby('road').agg(agg_functions).reset_index()

    df['number_of_tunnel'] = df['versjon'].apply(lambda x: len(x))

    return df

def skjerm_aggregate(df):
    agg_functions = {
        'segmentlengde': sum
    }
    df['road'] = df['vref'].apply(lambda x: x.split("D")[0])
    df = df[['road','segmentlengde']].groupby('road').agg(agg_functions).reset_index()
    df = df.rename(columns={'segmentlengde': 'lengde'})

    return df

def main():
    traffic_df = pd.read_excel("traffic-mainroads.xlsx")
    traffic_df = traffic_aggregate(traffic_df)

    #Centrality
    with open('centralityDict.txt', 'r') as fp: 
        bc = json.load(fp)
    
    bc_list = [(key, value) for key, value in bc.items()]
    bc_df =  pd.DataFrame(bc_list, columns=['road', 'bc'])

    merged_df = pd.merge(traffic_df[['road', 'average_ådt']],bc_df, on='road',how='inner')
    
    #Feltoversikt
    """feltoversikt_df = pd.read_excel("feltoversikt-mainroads.xlsx") 
    feltoversikt_df = feltoversikt_aggregate(feltoversikt_df)

    merged_df = pd.merge(traffic_df[['road', 'average_ådt']],feltoversikt_df[['road', 'average_felt']], on='road',how='inner')"""
    
    #Bomstasjon
    """bomstasjon_df = pd.read_excel("bomstasjon-mainroads.xlsx")
    bomstasjon_df = bomstasjon_aggregate(bomstasjon_df)

    merged_df = pd.merge(traffic_df[['road', 'average_ådt']], bomstasjon_df[['road', 'total_takst']], on='road',how='inner')"""

    #Vertikalelement
    """vertikalelement_df = pd.read_excel("vertikalelement-mainroads.xlsx")
    vertikalelement_df = vertikalelement_aggregate(vertikalelement_df)

    merged_df = pd.merge(traffic_df[['road', 'average_ådt']], vertikalelement_df[['road', 'average_stigning']], on='road',how='inner')"""

    #Horisontalelement
    """horisontalelement_df = pd.read_excel("horisontalelement-mainroads.xlsx")
    horisontalelement_df = horisontalelement_aggregate(horisontalelement_df)

    merged_df = pd.merge(traffic_df[['road', 'average_ådt']], horisontalelement_df[['road', 'average_radius']], on='road',how='inner')"""

    #Midtdeler
    """midtdeler_df = pd.read_excel("midtdeler-mainroads.xlsx")
    midtdeler_df = midtdeler_aggregate(midtdeler_df)

    merged_df = pd.merge(traffic_df[['road', 'average_ådt','segmentlengde']], midtdeler_df[['road', 'lengde']], on='road',how='inner')
    merged_df['segmentlengde'] = merged_df['segmentlengde'].apply(lambda x: sum(x))
    merged_df['fylningsgrad'] = merged_df.apply(lambda x: x.lengde / x.segmentlengde,axis=1)"""

    #Stigning
    """stigning_df = pd.read_excel("stigning-mainroads.xlsx")
    stigning_df = stigning_aggregate(stigning_df)

    merged_df = pd.merge(traffic_df[['road', 'average_ådt']], stigning_df[['road', 'average_stigning']], on='road',how='inner')"""
    
    #Vegkryss
    """vegkryss_df = pd.read_excel("vegkryss-mainroads.xlsx")
    vegkryss_df = vegkryss_aggregate(vegkryss_df)

    merged_df = pd.merge(traffic_df[['road', 'average_ådt', 'segmentlengde']], vegkryss_df[['road', 'number_of_vegkryss']], on='road',how='inner')
    merged_df['segmentlengde'] = merged_df['segmentlengde'].apply(lambda x: sum(x))
    merged_df['vegkryssgrad'] = merged_df.apply(lambda x: x.number_of_vegkryss / x.segmentlengde,axis=1)"""

    #Motorveg
    """motorveg_df = pd.read_excel("motorveg-mainroads.xlsx")
    motorveg_df = motorveg_aggregate(motorveg_df)

    merged_df = pd.merge(traffic_df[['road', 'average_ådt','segmentlengde']], motorveg_df[['road', 'lengde']], on='road',how='inner')
    merged_df['segmentlengde'] = merged_df['segmentlengde'].apply(lambda x: sum(x))
    merged_df['fylningsgrad'] = merged_df.apply(lambda x: x.lengde / x.segmentlengde,axis=1)"""

    #Vegbredde
    """vegbredde_df = pd.read_excel("vegbredde-mainroads.xlsx")
    vegbredde_df = vegbredde_aggregate(vegbredde_df)

    merged_df = pd.merge(traffic_df[['road', 'average_ådt']], vegbredde_df[['road', 'average_dekkebredde']], on='road',how='inner')"""

    #Fartsdemper
    """fartsdemper_df = pd.read_excel("fartsdemper-mainroads.xlsx")
    fartsdemper_df = fartsdemper_aggregate(fartsdemper_df)

    merged_df = pd.merge(traffic_df[['road', 'average_ådt', 'segmentlengde']], fartsdemper_df[['road', 'number_of_fartsdemper']], on='road',how='inner')
    merged_df['segmentlengde'] = merged_df['segmentlengde'].apply(lambda x: sum(x))
    merged_df['fartsdempergrad'] = merged_df.apply(lambda x: x.number_of_fartsdemper / x.segmentlengde,axis=1)"""

    #Forkjørsveg
    """forkjørsveg_df = pd.read_excel("forkjørsveg-mainroads.xlsx")
    forkjørsveg_df = forkjørsveg_aggregate(forkjørsveg_df)

    merged_df = pd.merge(traffic_df[['road', 'average_ådt','segmentlengde']], forkjørsveg_df[['road', 'lengde']], on='road',how='inner')
    merged_df['segmentlengde'] = merged_df['segmentlengde'].apply(lambda x: sum(x))
    merged_df['fylningsgrad'] = merged_df.apply(lambda x: x.lengde / x.segmentlengde,axis=1)"""

    #Rasteplass
    """rasteplass_df = pd.read_excel("rasteplass-mainroads.xlsx")
    rasteplass_df = rasteplass_aggregate(rasteplass_df)

    merged_df = pd.merge(traffic_df[['road', 'average_ådt', 'segmentlengde']], rasteplass_df[['road', 'number_of_rasteplass']], on='road',how='inner')
    merged_df['segmentlengde'] = merged_df['segmentlengde'].apply(lambda x: sum(x))
    merged_df['rasteplassgrad'] = merged_df.apply(lambda x: x.number_of_rasteplass / x.segmentlengde,axis=1)"""

    #Rekkverk
    """rekkverk_df = pd.read_excel("rekkverk-mainroads.xlsx")
    rekkverk_df = rekkverk_aggregate(rekkverk_df)

    merged_df = pd.merge(traffic_df[['road', 'average_ådt','segmentlengde']], rekkverk_df[['road', 'lengde']], on='road',how='inner')
    merged_df['segmentlengde'] = merged_df['segmentlengde'].apply(lambda x: sum(x))
    merged_df['fylningsgrad'] = merged_df.apply(lambda x: x.lengde / x.segmentlengde,axis=1)"""

    #Skiltpunkt
    """skiltpunkt_df = pd.read_excel("skiltpunkt-mainroads.xlsx")
    skiltpunkt_df = skiltpunkt_aggregate(skiltpunkt_df)

    merged_df = pd.merge(traffic_df[['road', 'average_ådt', 'segmentlengde']], skiltpunkt_df[['road', 'number_of_skiltpunkt']], on='road',how='inner')
    merged_df['segmentlengde'] = merged_df['segmentlengde'].apply(lambda x: sum(x))
    merged_df['skiltpunktgrad'] = merged_df.apply(lambda x: x.number_of_skiltpunkt / x.segmentlengde,axis=1)"""

    #Fartsgrense
    """fartsgrense_df = pd.read_excel("fartsgrense-mainroads.xlsx")
    fartsgrense_df = fartsgrense_aggregate(fartsgrense_df)

    merged_df = pd.merge(traffic_df[['road', 'average_ådt']], fartsgrense_df[['road', 'average_fartsgrense']], on='road',how='inner')"""

    #Segmentlengde
    """merged_df = traffic_df.copy()
    merged_df['segmentlengde'] = merged_df['segmentlengde'].apply(lambda x: sum(x))"""

    #Tunnel
    """tunnel_df = pd.read_excel("tunnel-mainroads.xlsx")
    tunnel_df = tunnel_aggregate(tunnel_df)

    merged_df = pd.merge(traffic_df[['road', 'average_ådt', 'segmentlengde']], tunnel_df[['road', 'number_of_tunnel']], on='road',how='inner')
    merged_df['segmentlengde'] = merged_df['segmentlengde'].apply(lambda x: sum(x))
    merged_df['tunnelgrad'] = merged_df.apply(lambda x: x.number_of_tunnel / x.segmentlengde,axis=1)"""

    #Skjerm
    """skjerm_df = pd.read_excel("skjerm-mainroads.xlsx")
    skjerm_df = skjerm_aggregate(skjerm_df)

    merged_df = pd.merge(traffic_df[['road', 'average_ådt','segmentlengde']], skjerm_df[['road', 'lengde']], on='road',how='inner')
    merged_df['segmentlengde'] = merged_df['segmentlengde'].apply(lambda x: sum(x))
    merged_df['fylningsgrad'] = merged_df.apply(lambda x: x.lengde / x.segmentlengde,axis=1)"""

    merged_df.plot.scatter(x='average_ådt', y='bc', color='blue')
    plt.show()
    corr = merged_df['average_ådt'].corr(merged_df['bc'])
    print(corr)

    """ådt = pd.Series(sorted([x for x in merged_df['average_ådt'].values.tolist() if not math.isnan(x)]))
    #bc = pd.Series(sorted([x for x in merged_df['bc'].values.tolist() if not math.isnan(x)]))
    
    ådt.plot(kind='line', linestyle='-')
    plt.show()"""

    """bc.plot(kind='line', linestyle='-')
    plt.show()"""


if __name__ == "__main__":
    main()
    #download_skjerm()