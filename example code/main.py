from node import Node
from trees import build_dfs
import random
import math
# from dsa_scheduling import get_eligible_nodes
import matplotlib.pyplot as plt
import numpy as np

duty_cycle = 3

def distance (node1, node2):
    return math.sqrt(pow((node1.x-node2.x), 2) + pow((node1.y-node2.y), 2))

def count_Cv(node, child):
    count = 0
    for child in node.childrenIDs:
        count += 1
        count += count_Cv(node, child)
        
    return count

# def build_MLST(node_list):
#     tree = []
#     tree.append(node_list[0])
#     while 

def isDuplicate(node_list, x, y, radius):
    for node in node_list:
        dist = math.sqrt((node.x - x) ** 2 + (node.y - y) ** 2)
        if dist <= radius:
            return True
    return False


# def build_DFS(node_list):
#     stack = [0]  # Initialize the stack with the root node ID
#     while stack:
#         current_node_id = stack.pop()
#         current_node = node_list[current_node_id]
#         current_node.discovered = True

#         for neighbor_id in current_node.neighbors:
#             neighbor_node = node_list[neighbor_id]
#             if not neighbor_node.discovered:
#                 neighbor_node.parentID = current_node_id
#                 neighbor_node.distance = current_node.distance + 1
#                 stack.append(neighbor_id)

def build_DFS(node_list):
    list = [0]
    while len(list) > 0:
        v = list[-1]
        list.remove(v)
        if node_list[v].discovered is False:
            node_list[v].discovered = True
            for k in node_list[v].neighbors:
                if k not in list and node_list[k].discovered is False:
                    node_list[k].parentID = v
                    node_list[v].childrenIDs.append(k)
                    list.append(k)
        
def print_tree(node_list):
    for node in node_list:
        print(f"Node ID: {node.ID}, Parent ID: {node.parentID}")    


def simple_scheduling(node_list, duty_cycle):
    t = 0
    Sf = []
    while len(Sf) < len(node_list) - 1:  # Exclude the sink node
        eligible_nodes, _ = get_eligible_nodes(node_list, duty_cycle, t)
        sorted_eligible_nodes = sorted(eligible_nodes, key=lambda x: node_list[x].dcat_weight, reverse=True)

        S = []
        R = []
        for u in sorted_eligible_nodes:
            if u not in R:
                if is_collision_free(node_list, S, R, u, t):
                    S.append(u)
                    R.extend(node_list[u].neighbors)
        
        Sf += S
        t += 1
    print(f"""t = {t}
S: {u}
R: {R}""")
    return t

def get_eligible_nodes(node_list, duty_cycle, time_now):
    eligible_nodes = []
    scheduled = []
    for u in node_list:
        if u.tx_wp == -1:  # u is not assigned a transmitting working period
            if len(u.childrenIDs) > 0:  # u has child(ren)
                for c in u.childrenIDs:
                    if node_list[c].tx_wp == -1:
                        break
                else:
                    eligible_nodes.append(u.ID)
            else:
                eligible_nodes.append(u.ID)
        else:
            scheduled.append(u.ID)
    return eligible_nodes, scheduled

def is_collision_free(node_list, S, R, u, t):
    for v in node_list[u].neighbors:
        if v in S and node_list[v].timeslot == t % duty_cycle:
            return False
    for w in node_list[u].neighbors:
        if w in R and node_list[w].timeslot == t % duty_cycle:
            for x in node_list[w].neighbors:
                if x in S and node_list[x].timeslot == t % duty_cycle:
                    return False
    return True
   

if __name__ == "__main__":
# Generate a list of nodes
    N = 400  # number of nodes
    X = 200  # X-dimension
    Y = 200  # Y-dimension
    R = 30   # communication range
    
    node_list = []
    for i in range(0, N):
        # generate a node
        node = Node()
        node.ID = i
        node.x = random.uniform(0, X)
        node.y = random.uniform(0, X)

        # check duplication?
        for k in node_list:
            if k.x != node.x and k.y != node.y:
                continue
            else:   
                print("collision")
                node.x = random.uniform(0,X)
                node.y = random.uniform(0,X)

        node_list.append(node)
        pass
    # Check for node's location.
    for node in node_list:
        print(f"Node ID: {node.ID}, X: {node.x}, Y: {node.y}")

# Update neighbors
    # loop through node_list
    for i in range(len(node_list)):
        for j in range(i+1, len(node_list)):
                dist = distance(node_list[i], node_list[j])
                # check distance < 30
                if dist < R:
                    node_list[i].neighbors.append(j) # update node's neighbor
                    node_list[j].neighbors.append(i)

    for node in node_list:
        print(f"node ID: {node.ID}, neighbors: {node.neighbors}")

    # Build a tree on the node_list
    build_DFS(node_list)
    print_tree(node_list)

    time = simple_scheduling(node_list, duty_cycle)
    # print(time)

    for node in node_list:
        plt.scatter(node.x, node.y , marker = 'x', c = 'r')
        plt.annotate(node.ID, (node.x,node.y))
    plt.title("Node positions")    
    plt.show()

    pass