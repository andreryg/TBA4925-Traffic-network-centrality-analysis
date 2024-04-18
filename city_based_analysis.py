from initial_analysis import read_csv_to_dataframe, road_grouping, speedlimit_grouping, centroid, create_adjacency_list 
from initial_analysis import calculate_centrality, create_color_map
from tqdm import tqdm
import geopandas as gpd
import pandas as pd
import json
import networkx as nx
import matplotlib.pyplot as plt

def main():
    tettsteder = read_csv_to_dataframe("alle_tettsteder.csv")
    for row in tqdm(tettsteder.itertuples(), total=tettsteder.shape[0]):
        speedlimit_df = read_csv_to_dataframe(f"city_data/speedlimit_{row.tettstednavn.replace('/','&')}.csv")
        speedlimit_df = speedlimit_grouping(speedlimit_df)
        road_df = read_csv_to_dataframe(f"city_data/veg_{row.tettstednavn.replace('/','&')}.csv")
        road_df = road_grouping(road_df)

        road_gdf = gpd.GeoDataFrame(road_df, geometry='geometry', crs=5973)
        road_gdf = pd.merge(road_gdf, speedlimit_df, on='road', how='left')
        road_gdf['fjern'] = road_gdf['road'].apply(lambda x: 1 if len(x) < 6 else 0)
        road_gdf = road_gdf.loc[road_gdf['fjern'] == 0]
        road_gdf['time'] = road_gdf['time'].fillna(1) #TODO accurate time values for ferry segments.
        road_gdf['road_centroid'] = road_gdf['geometry'].apply(lambda x: centroid(x))
        road_gdf['x'] = road_gdf['road_centroid'].apply(lambda x: x.x)
        road_gdf['y'] = road_gdf['road_centroid'].apply(lambda x: x.y)

        """print("creating adjancency list")
        path = f"city_data/adjacencyDict_{row.tettstednavn.replace('/','&')}.txt"
        print(path)"""
        """adjacents = create_adjacency_list(road_gdf)
        with open(f"city_data/adjacencyDict_{row.tettstednavn.replace('/','&')}.txt", 'w') as fp:
            json.dump(adjacents, fp)"""
        with open(f"city_data/adjacencyDict_{row.tettstednavn.replace('/','&')}.txt", 'r') as fp:
            adjacents = json.load(fp)

        road_gdf['pos'] = road_gdf.apply(lambda x: (x.x,x.y),axis=1)
        road_gdf['color'] = road_gdf['road'].apply(lambda x: 'red' if x[0] in ["R", "E"] else 'black')

        G = nx.DiGraph(adjacents)
        nx.set_node_attributes(G, road_gdf[['road','x','y','color']].set_index('road').to_dict('index'))
        for pair in list(G.edges):
            G.edges[pair[0],pair[1]]["weight"] = round((1/(road_gdf[road_gdf['road'] == pair[1]]['time']))*100).values
        G.remove_edges_from(nx.selfloop_edges(G))

        print("calculating centrality...")
        G, bc = calculate_centrality(G)
        print("done")
        with open(f"city_data/centralityDict_{row.tettstednavn.replace('/','&')}.txt", 'w') as fp:
            json.dump(bc, fp)

        print(row.tettstednavn.replace('/','&'))

        """G = G.subgraph([x for x,y in G.nodes(data=True) if "x" not in x])
        colors = ['#377eb8', '#feb24c', '#e41a1c']
        color_map, color_dict, labels = create_color_map(G, colors)

        road_gdf['color'] = road_gdf.road.map(color_dict)
        road_gdf.plot(color=road_gdf['color'])
        plt.show()"""



if __name__ == "__main__":
    main()