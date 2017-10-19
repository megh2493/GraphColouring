import copy
import mapnode
import node
import player
import sys


# function to generate the child maps
def get_child_map(parent_map, cur_player):
    player_nodes = parent_map["map"].get_player_to_state()
    playerA_node = player_nodes[0]["playerA"]
    playerB_node = player_nodes[0]["playerB"]
    all_nodes = parent_map["map"].get_nodes_list()
    mapList = []
    colored_nodes = list(set(playerA_node) | set(playerB_node))
    neighbor_nodes = set()
    temp_node_list = []

    # check if occupied nodes is in all existing nodes and set it as adjacent nodes
    for cnode in colored_nodes:
        for anode in all_nodes:
            if cnode.get_name() is anode.get_name():
                neighbor_nodes = neighbor_nodes.union(anode.get_neighbors())
    # removes colored node from neighbor node
    neighbor_nodes = neighbor_nodes - set([m.get_name() for m in colored_nodes])
    for m in all_nodes:
        if m.get_name() in neighbor_nodes:
            temp_node_list.append(m)

    # sort the nodes names in alphabetical order
    sorted_list = sorted(temp_node_list, key=lambda n: n.get_name())

    # iterate through the sorted list find the next node to be colored and add it to child nodes of map
    for node in sorted_list:
        player = None
        child_map = None
        available_colors = node.get_domain()
        # sorting colors in domain value
        for color in sorted(available_colors):
            # make a copy of node
            next_node = copy.deepcopy(node)

            # make a copy of map
            child_map = copy.deepcopy(parent_map["map"])

            next_node.set_color(color)
            next_node.set_assigned_player(cur_player)

            # update the nodes colored by players
            players = child_map.get_players()
            for p in players:
                if p.get_name() == cur_player:
                    p.update_player_moves(next_node, color)

            # update the child_nodes in the child map
            for chnode in child_map.get_nodes_list():
                if chnode.get_name() == next_node.get_name():
                    if next_node.get_neighbors() is None:
                        next_node.set_neighbors(chnode.get_neighbors())
            child_map.set_player_to_state_value(cur_player, next_node)

            adj_nodes = next_node.get_neighbors()
            map_node_lists = child_map.get_nodes_list()

            # update the domain of the adjacent nodes
            for i in map_node_lists:
                if i.get_color() is None:
                    if i.get_name() in adj_nodes:
                        temp_domain = i.get_domain()
                        if color in temp_domain:
                            temp_domain.remove(color)

            for node1 in child_map.get_nodes_list():
                if node1.get_name() == next_node.get_name():
                    child_map.get_nodes_list().remove(node1)
            child_map.get_nodes_list().append(next_node)
            return_data = {}

            return_data["map"] = child_map
            return_data["node"] = next_node
            return_data["colorValue"] = color
            mapList.append(return_data)

    return mapList


# alpha beta pruning to determine the best possible action
def alpha_beta_search(mapHistory, maxDepth):
    # pruning to perform when max node is reached
    def max_node(max_map, alpha, beta, cur_depth, maxDepth):
        vector = -float('inf')
        colored_max_nodes = None
        max_color_value = None

        # terminal cases to be checked
        if max_map["map"].terminal_test() or int(cur_depth) >= int(maxDepth):
            max_map["map"].utility_function()
            temp_string = max_map["node"].get_name(), max_map["colorValue"], cur_depth, max_map["map"].get_map_value(), alpha, beta
            print_string = ", ".join(map(str, temp_string))
            f.write(print_string)
            f.write("\n")
            return max_map["map"].get_map_value(), max_map["node"].get_name(), max_map["colorValue"]
        else:
            temp_string = max_map["node"].get_name(), max_map["colorValue"], cur_depth, str(vector), alpha, beta
            print_string = ", ".join(map(str, temp_string))
            f.write(print_string)
            f.write("\n")

        # generating children map node
        for child_map in get_child_map(max_map, "playerA"):
            # get the value, node and colorAssigned from min player
            value, colored_min_nodes, min_color_value = min_node(child_map, alpha, beta, int(cur_depth) + 1, maxDepth)

            # pruning
            if vector < value:
                colored_max_nodes = child_map["node"].get_name()
                max_color_value = child_map["colorValue"]
                vector = value

            if vector >= beta:
                temp_string = max_map["node"].get_name(), max_map["colorValue"], cur_depth, str(vector), alpha, beta
                print_string = ", ".join(map(str, temp_string))
                f.write(print_string)
                f.write("\n")
                return vector, colored_max_nodes, max_color_value
            alpha = max(alpha, vector)
            temp_string = max_map["node"].get_name(), max_map["colorValue"], cur_depth, str(vector), alpha, beta
            print_string = ", ".join(map(str, temp_string))
            f.write(print_string)
            f.write("\n")

        return vector, colored_max_nodes, max_color_value

    def min_node(min_map, alpha, beta, cur_depth, maxDepth):
        vector = float('inf')
        colored_min_nodes = None
        min_color_value = None

        # terminal cases to be checked
        if min_map["map"].terminal_test() or int(cur_depth) >= int(maxDepth):
            min_map["map"].utility_function()
            temp_string = min_map["node"].get_name(), min_map["colorValue"], cur_depth, min_map["map"].get_map_value(), alpha, beta
            print_string = ", ".join(map(str, temp_string))
            f.write(print_string)
            f.write("\n")
            return min_map["map"].get_map_value(), min_map["node"].get_name(), min_map["colorValue"]
        else:
            temp_string = min_map["node"].get_name(), min_map["colorValue"], cur_depth, str(vector), alpha, beta
            print_string = ", ".join(map(str, temp_string))
            f.write(print_string)
            f.write("\n")
        # generating children map node
        for child_map in get_child_map(min_map, "playerB"):
            # get the value, node and colorAssigned from max player
            value, colored_min_nodes, min_color_value = max_node(child_map, alpha, beta, int(cur_depth) + 1, maxDepth)

            # pruning
            if vector > value:
                colored_min_nodes = child_map["node"].get_name()
                min_color_value = child_map["colorValue"]
                vector = value

            if vector <= alpha:
                temp_string = min_map["node"].get_name(), min_map["colorValue"], cur_depth, str(vector), alpha, beta
                print_string = ", ".join(map(str, temp_string))
                f.write(print_string)
                f.write("\n")
                return vector, colored_min_nodes, min_color_value
            beta = min(beta, vector)
            temp_string = min_map["node"].get_name(), min_map["colorValue"], cur_depth, str(vector), alpha, beta
            print_string = ", ".join(map(str, temp_string))
            f.write(print_string)
            f.write("\n")

        # return final node value - best for max player
        return vector, colored_min_nodes, min_color_value

    cur_value, next_node, next_color = max_node(mapHistory, -float('inf'), float('inf'), 0, maxDepth)
    temp_string = next_node, next_color, cur_value
    print_string = ", ".join(map(str, temp_string))
    f.write(print_string)
    f.write("\n")

# initializations
rootMap = []
startMap = mapnode.MapNode()
domainValListA = {}
domainValListB = {}
playerA = player.Player("max", "playerA")
playerB = player.Player("min", "playerB")
nodeHistory = {playerA.name: [], playerB.name: []}
mapHistory = {}
temp_players = [playerA, playerB]

inputFile = open("sampleinput.txt", "r").readlines()
inputFile = [i.strip("\n") for i in inputFile]
listOfColors = inputFile[0].split(", ")
initialMoves = inputFile[1].split(", ")
initialColoring = [i.split("-") for i in initialMoves]

# creation of start map
for i in initialColoring:
    i[0] = i[0].split(": ")
for i in initialColoring:
    temp1 = [j for k in i for j in k]
    rootMap.append(temp1)
for i in rootMap:
    x = node.Node(i[0], i[1], None, copy.deepcopy(listOfColors), None)
    if int(i[2]) == 1:
        playerA.update_player_moves(x, i[1])
        x.set_assigned_player(playerA.get_name())
        nodeHistory[playerA.name].append(x)
    elif int(i[2]) == 2:
        playerB.update_player_moves(x, i[1])
        x.set_assigned_player(playerB.get_name())
        nodeHistory[playerB.name].append(x)
    startMap.set_nodes_list(x)
    startMap.set_players(temp_players)

    # IMPORTANT map history to know previous coloured values
    mapHistory["node"] = x
    mapHistory["colorValue"] = i[1]
startMap.set_player_to_state(nodeHistory)

maxDepth = inputFile[2]
# player 1 preferences
domainListA = inputFile[3].split(", ")
for i in domainListA:
    key1 = i.split(": ")
    domainValListA[key1[0]] = key1[1]
playerA.set_preference(domainValListA)

# player 2 preferences
domainListB = inputFile[4].split(", ")
for i in domainListB:
    key1 = i.split(": ")
    domainValListB[key1[0]] = key1[1]
playerB.set_preference(domainValListB)

# loop over all files to construct the root Map(list of nodes and colors available)
temp = inputFile[5:]
for i in temp:
    exists = False
    key = i.split(": ")
    children = key[1].split(", ")
    cur_nodes = startMap.get_nodes_list()
    # update neighbors for existing root map nodes
    for x in cur_nodes:
        if key[0] == x.get_name():
            exists = True
            for j in children:
                x.set_single_neighbor(j)
    # add remaining nodes to root map node
    if exists is not True:
        temp_node = node.Node(key[0], None, None, copy.deepcopy(listOfColors), None)
        for j in children:
            temp_node.set_single_neighbor(j)
        # update domain value based on available values
        for child in children:
            for temp in cur_nodes:
                if temp.get_name() == child:
                    temp_dom = temp_node.get_domain()
                    if temp.get_color() is not None:
                        temp_dom.remove(temp.get_color())
                    temp_node.set_domain(temp_dom)
        startMap.set_nodes_list(temp_node)
# IMPORTANT map history to know previous maps
mapHistory["map"] = startMap
f = open("output.txt", "w")
alpha_beta_search(mapHistory, maxDepth)
f.close()
