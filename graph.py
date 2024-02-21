import matplotlib.pyplot as plt

class Node(object):
    def __init__(self, x, y, id, color):
        self.x = x
        self.y = y
        self.id = id
        self.color = color

    def set_centrality(self, centrality):
        self.centrality = centrality

    def get_centrality(self):
        return self.centrality
    
    def get_coordinates(self):
        return [self.x, self.y]
    
    def plotting(self):
        plt.plot(self.x, self.y, 'o', color=self.color)

class CityNode(Node):
    def __init__(self, x, y, id, color, population, name):
        super().__init__(x, y, id, color)
        self.population = population
        self.name = name

class TransportNode(Node):
    def __init__(self, x, y, id, color, weight, road_id):
        super().__init__(x, y, id, color)
        self.weight = weight
        self.road_id = road_id
    
class Edge(object):
    def __init__(self, id_from, id_to, id):
        self.id_from = id_from
        self.id_to = id_to
        self.id = id

    