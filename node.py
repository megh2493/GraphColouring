class Node:
    def __init__(self, name=None, color=None, assigned_player=None, domain=None, neighbors=None):
        self.name = name
        self.color = color
        self.domain = domain
        self.neighbors = []
        self.assigned_player = assigned_player

    def get_neighbors(self):
        return self.neighbors

    def set_neighbors(self, value):
        self.neighbors.extend(value)

    def get_assigned_player(self):
        return self.assigned_player

    def set_assigned_player(self, value):
        self.assigned_player = value

    def set_single_neighbor(self, value):
        self.neighbors.append(value)

    def get_color(self):
        return self.color

    def set_color(self, value):
        self.color = value

    def get_domain(self):
        return self.domain

    def set_domain(self, value):
        self.domain = value

    def get_name(self):
        return self.name

    def set_name(self, value):
        self.name = value

    def __repr__(self):
        return "name:" + self.name + " color: " + str(self.color) + " player: " + str(self.assigned_player) + " domain: " + str(self.domain) + " neighbor: " + str(self.neighbors)

