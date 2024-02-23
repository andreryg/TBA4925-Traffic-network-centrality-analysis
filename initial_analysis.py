import pandas as pd
import geopandas as gpd
from shapely import wkt
from shapely.ops import linemerge
import matplotlib.pyplot as plt
import math
from graph import CityNode, TransportNode
import pickle
import json
import networkx as nx

def read_excel_to_dataframe(file):
    return pd.read_excel(file)

def read_csv_to_dataframe(file):
    return pd.read_csv(file)

def wkt_loads(x):
    try:
        return wkt.loads(x)
    except Exception:
        return None

def centroid(polygon):
    return polygon.centroid

def speedlimit_grouping(speedlimit_dataframe):
    agg_functions = {
        'time': sum,
    }
    speedlimit_dataframe['road'] = speedlimit_dataframe['vref'].apply(lambda x: x.split("D")[0])
    speedlimit_dataframe['time'] = speedlimit_dataframe.apply(lambda x: (float(x.segmentlengde)/1000)/float(x.Fartsgrense), axis=1)
    speedlimit_dataframe = speedlimit_dataframe[['road', 'time']].groupby('road').agg(agg_functions).reset_index()

    return speedlimit_dataframe

def road_grouping(road_dataframe):
    agg_functions = {
        'geometry': '- '.join,
        'startnode': ', '.join,
        'sluttnode': ', '.join
    }
    road_dataframe['road'] = road_dataframe['vref'].apply(lambda x: x.split("D")[0])
    road_dataframe = road_dataframe[['road','startnode','sluttnode','geometry']].groupby('road').agg(agg_functions).reset_index()
    #print(road_dataframe.shape)

    for index, row in road_dataframe.iterrows():
        value = row['geometry']
        for y in value.split('- '):
            try:
                wkt.loads(y)
            except Exception:
                print(f'{index} [{len(value)}] {y}')
    road_dataframe['noder'] = road_dataframe.apply(lambda x: [i.replace(" ","") for i in x.startnode.split(',') + x.sluttnode.split(',')], axis=1)
    road_dataframe = road_dataframe.drop(columns=['startnode', 'sluttnode'])
    #road_dataframe['noder'] = road_dataframe['startnode'] + ', ' + road_dataframe['sluttnode']
    #road_dataframe['noder'] = road_dataframe['noder'].apply(lambda x: list(set(x.split(', '))))

    road_dataframe['geometry'] = road_dataframe['geometry'].apply(lambda x: linemerge([wkt_loads(y) for y in x.split('- ')]))
    return road_dataframe

def create_adjacency_list(road_dataframe):
    """
    Takes a dataframe of road segments and returns a dictionary of adjacency list graph representation.
    """
    adjacency_list = {}

    for ind in road_dataframe.index:
        adjacents = []
        for node in road_dataframe['noder'][ind]:
            adj_noder = road_dataframe.loc[road_dataframe['noder'].apply(lambda x: node in x)]
            adjacents += adj_noder['road'].values.tolist()
        adjacents = list(set(adjacents))
        try:
            adjacents.remove(road_dataframe['road'][ind])
        except:
            pass
        adjacency_list.update({road_dataframe['road'][ind] : adjacents})

    return adjacency_list

def pop_function(x):
    return math.sqrt(x)/5

def create_color_map(G, colors):
    color_map = []
    color_dict = {}
    bc_list = []
    for node in G:
        bc_list.append(G.nodes[node]["cent_betweenness"])
    n = math.ceil(len(bc_list)/3)
    bc_list = sorted(bc_list)
    split1 = 70
    split2 = 95
    final = [[],[],[]]
    for i,v in enumerate(bc_list):
        if i/len(bc_list) * 100 < split1:
            final[0].append(v)
        elif i/len(bc_list) * 100 < split2:
            final[1].append(v)
        else:
            final[2].append(v)
    #print(len(final[0]), len(final[1]), len(final[2]))
    
    for node in G:
        if G.nodes[node]["cent_betweenness"] in final[0]:
            color_map.append(colors[0])
            color_dict.update({node : colors[0]})
        elif G.nodes[node]["cent_betweenness"] in final[1]:
            color_map.append(colors[1])
            color_dict.update({node : colors[1]})
        else:
            color_map.append(colors[2])
            color_dict.update({node : colors[2]})
        """elif G.nodes[node]["cent_betweenness"] < 0.07:
            color_map.append(colors[2])
            color_dict.update({node : colors[2]})
        elif G.nodes[node]["cent_betweenness"] < 0.1:
            color_map.append(colors[3])
            color_dict.update({node : colors[3]})
        elif G.nodes[node]["cent_betweenness"] < 0.15:
            color_map.append(colors[4])
            color_dict.update({node : colors[4]})
        elif G.nodes[node]["cent_betweenness"] < 0.2:
            color_map.append(colors[5])
            color_dict.update({node : colors[5]})"""
    labels={'#377eb8':f"Centrality: [{format(final[0][0], '.4f')}, {format(final[0][-1], '.4f')}]", '#feb24c':f"Centrality: [{format(final[1][0], '.4f')}, {format(final[1][-1], '.4f')}]", '#e41a1c':f"Centrality: [{format(final[2][0], '.4f')}, {format(final[2][-1], '.4f')}]"}
    return color_map, color_dict, labels

def calculate_centrality(G):
    bc = nx.betweenness_centrality(G)
    nx.set_node_attributes(G, bc, "cent_betweenness")
    return G, bc

def main():
    speedlimit_dataframe = read_csv_to_dataframe("speedlimit.csv")
    speedlimit_dataframe = speedlimit_grouping(speedlimit_dataframe)
    
    road_dataframe = read_csv_to_dataframe("veg.csv")
    road_dataframe = road_grouping(road_dataframe)

    road_gdf = gpd.GeoDataFrame(road_dataframe, geometry='geometry', crs=5973)
    """gdf.plot()
    plt.show()"""

    tettsteder = read_csv_to_dataframe("alle_tettsteder.csv")
    tettsteder['geometry'] = tettsteder['geometry'].apply(lambda x: wkt.loads(x))
    tettsteder_gdf = gpd.GeoDataFrame(tettsteder, geometry='geometry', crs=5973)
    #tettsteder_gdf['centroid'] = tettsteder_gdf['geometry'].apply(lambda x: centroid(x))
    """tettsteder_gdf.plot()
    plt.show()"""

    #road_gdf = road_gdf.overlay(tettsteder_gdf, how='union')
    road_gdf = gpd.sjoin(left_df=road_gdf,right_df=tettsteder_gdf,how='left')
    road_gdf = pd.merge(road_gdf, speedlimit_dataframe, on='road', how='left')
    road_gdf['fjern'] = road_gdf['road'].apply(lambda x: 1 if len(x) < 6 else 0)
    road_gdf = road_gdf.loc[road_gdf['fjern'] == 0]
    road_gdf['time'] = road_gdf['time'].fillna(1) #TODO accurate time values for ferry segments.
    road_gdf['road_centroid'] = road_gdf['geometry'].apply(lambda x: centroid(x))
    road_gdf['x'] = road_gdf['road_centroid'].apply(lambda x: x.x)
    road_gdf['y'] = road_gdf['road_centroid'].apply(lambda x: x.y)
    road_gdf['color'] = road_gdf['tettstednummer'].apply(lambda x: 'red' if not math.isnan(float(x)) else 'black')
    road_gdf['road'] = road_gdf.apply(lambda x: x.road+'_'+x.tettstednavn if not math.isnan(float(x.tettstednummer)) else x.road, axis=1)
    cities = list(set(road_gdf['tettstednavn'].values))
    cities = [x for x in cities if x == x]
    extra = 0
    road_x_gdf = pd.DataFrame(columns=road_gdf.columns)
    for city in cities:
        city_gdf = road_gdf.loc[road_gdf['tettstednavn'] == city]
        pop = round(pop_function(float(city_gdf['totalBefolkning'].values[0])))
        div = pop // city_gdf.shape[0]
        pop = div * city_gdf.shape[0] + round((pop % city_gdf.shape[0])/city_gdf.shape[0]) * city_gdf.shape[0] - city_gdf.shape[0]
        extra += pop
        a = round(pop / city_gdf.shape[0])
        for i in range(a):
            temp_city_gdf = city_gdf.copy()
            temp_city_gdf['road'] = temp_city_gdf['road'].apply(lambda x: x+'x'+str(i))
            road_x_gdf = pd.concat([road_x_gdf, temp_city_gdf], ignore_index=True)
    print("Legger til ",extra," ekstra noder")
    #road_x_gdf.to_excel("ttttest.xlsx") 

    """adjacents = create_adjacency_list(road_gdf)
    with open('adjacencyDict.txt', 'w') as fp:
        json.dump(adjacents, fp)"""
    with open('adjacencyDict.txt', 'r') as fp:
        adjacents = json.load(fp)

    for i in road_x_gdf['road'].values.tolist():
        if i.split("x")[0] in adjacents:
            adjacents[i] = adjacents.get(i.split("x")[0])
        else:
            print(i)
    road_gdf = pd.concat([road_gdf, road_x_gdf], ignore_index=True)
    road_gdf['pos'] = road_gdf.apply(lambda x: (x.x,x.y),axis=1)
    pos = dict(zip(road_gdf.road,road_gdf.pos))

    G = nx.DiGraph(adjacents)
    
    nx.set_node_attributes(G, road_gdf[['road','x','y','color']].set_index('road').to_dict('index'))
    for pair in list(G.edges):
        G.edges[pair[0],pair[1]]["weight"] = round((2 - road_gdf[road_gdf['road'] == pair[1]]['time'])*100)
    G.remove_edges_from(nx.selfloop_edges(G))
    
    print(list(G.neighbors("EV6 S3_Fredrikstad/Sarpsborgx1")))
    G, bc = calculate_centrality(G)
    with open('centralityDict.txt', 'w') as fp:
        json.dump(bc, fp)

    colors = ['#377eb8', '#feb24c', '#e41a1c']
    color_map, color_dict, labels = create_color_map(G, colors)


    fig, ax = plt.subplots()
    nx.draw(G,pos=pos,node_color=color_map,ax=ax)#[nx.get_node_attributes(G,'color')[node] for node in G.nodes()],ax=ax)
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.show()

    
    #road_gdf.to_excel("ttttest.xlsx") 
    """
    road_gdf['road_centroid'] = road_gdf['geometry'].apply(lambda x: centroid(x))
    road_gdf['color'] = road_gdf['tettstednummer'].apply(lambda x: 'red' if not math.isnan(float(x)) else 'black')
    road_gdf.plot(color=road_gdf['color'])
    plt.show()

    list_of_city_nodes = [CityNode(i.centroid.x, i.centroid.y, i.tettstednummer, i.color, i.totalBefolkning, i.tettstednavn) for i in road_gdf[road_gdf['centroid'].notnull()].itertuples()] 
    list_of_transport_nodes = [TransportNode(i.road_centroid.x, i.road_centroid.y, 1, i.color, 1, 1) for i in road_gdf[road_gdf['centroid'].isnull()].itertuples()]
    #for node in list_of_transport_nodes:
     # node.plotting()
    road_gdf[road_gdf['centroid'].isnull()].plot()
    for node in list_of_city_nodes:
        node.plotting()
    plt.show()"""

main()