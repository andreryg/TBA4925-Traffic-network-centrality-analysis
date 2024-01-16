
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
    
class Edge(object):
    def __init__(self, id_from, id_to, id):
        self.id_from = id_from
        self.id_to = id_to
        self.id = id

    