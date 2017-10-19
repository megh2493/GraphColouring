import copy
class MapNode:
    def __init__(self, nodes_list=None, player_to_state=None, map_value=None, players=None):
        self.player_to_state = player_to_state
        self.players = players
        self.map_value = map_value
        if nodes_list is None:
            self.nodes_list = []
        else:
            self.nodes_list = nodes_list

    def get_players(self):
        return self.players

    def set_players(self, value):
        self.players = value

    def get_map_value(self):
        return self.map_value

    def set_map_value(self, value):
        self.map_value = value

    def get_nodes_list(self):
        return self.nodes_list

    def set_nodes_list(self, value):
        self.nodes_list.append(value)

    def get_player_to_state(self):
        return self.player_to_state

    def set_player_to_state(self, value):
        self.player_to_state = []
        self.player_to_state.append(value)

    def set_player_to_state_value(self, player, value):
        stateList = self.player_to_state[0][player]
        stateList.append(value)

    def utility_function(self):
        playerA_val = 0
        playerB_val = 0
        for player, nodes in self.player_to_state[0].iteritems():
            if player == "playerA":
                for node in nodes:
                    for color, color_weightage in self.players[0].get_preference().iteritems():
                        if color == node.color:
                            playerA_val += int(copy.deepcopy(color_weightage))

            elif player is "playerB":
                for node in nodes:
                    for color, color_weightage in self.players[1].get_preference().iteritems():
                        if color == node.color:
                            playerB_val += int(copy.deepcopy(color_weightage))

        self.map_value = int(playerA_val) - int(playerB_val)

    def terminal_test(self):
        states = self.player_to_state[0]
        playerA_nodes = states['playerA']
        playerB_nodes = states['playerB']
        if len(self.nodes_list) == len(playerA_nodes) + len(playerB_nodes):
            return True
        else:
            return False

    def __repr__(self):
        return str(self.nodes_list) + " playertostate: " + str(self.player_to_state)

