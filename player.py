class Player:

    def __init__(self, type, name, preference=None, node_colored=None, points=0):
        self.type = type
        self.name = name
        self.node_colored = []
        self.preference = {}
        self.points = points

    def update_player_moves(self, node, color):
        self.node_colored.append(node)
        for key, value in self.preference.items():
            if key == color:
                self.points += int(value)

    def get_type(self):
        return self.type

    def set_type(self, value):
        self.type = value

    def get_name(self):
        return self.name

    def set_name(self, value):
        self.name = value

    def get_preference(self):
        return self.preference

    def set_preference(self, value):
        self.preference = value

    def get_node_colored(self):
        return self.node_colored

    def get_points(self):
        return self.points

    def __repr__(self):
        return "name: " + self.name + " type: " + self.type + " nodes: " + str(self.node_colored)
