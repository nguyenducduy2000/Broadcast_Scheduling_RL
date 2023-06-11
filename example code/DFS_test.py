from node import Node
# from trees import build_dfs
import random
import math
from dsa_scheduling import get_eligible_nodes

def distance (node1, node2):
    print("distance: " + str(math.sqrt(pow((node1.x-node2.x), 2) + pow((node1.y-node2.y), 2))))
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
        node.x = random.uniform(0, 200)
        node.y = random.uniform(0,200)

        # check duplication?
        for k in node_list:
            if k.x != node.x and k.y != node.y:
                continue
            else:   
                print("collision")
                node.x = random.uniform(0,200)
                node.y = random.uniform(0,200)
                          
        node_list.append(node)
        pass

    # Update neighbors
        # loop through node_list
        # check distance < 30
        # node_list[i].neighbors.append(<id>)
    for i in range(0,N):
        for k in range(1,N):
            if(distance(node_list[i], node_list[k]) < 30):
                
                node_list[i].neighbors.append(k)
        
    # Build a tree on the node_list
    build_DFS(node_list)
    for list in node_list:
        print(list.neighbors)
        print(str(list.x) + " and " + str(list.y))

    # Do some scheduling algorithm
        # Iterative
        # Per time slot: get eligible nodes (nodes that can be scheduled--> exclude s
            # <loop>
                #  Traverse the list of eligible nodes (one by one)
                #  Forbid potentially collided transmissions (related neighbors of the considering node)
                # → Avoid primary and secondary collisions
            # <end-loop>

    t = 0
    scheduled_nodes = []
    while( len(scheduled_nodes) < N-1): # both broadcast and aggergation: exclude sink (source) node
        eligible_nodes = get_eligible_nodes(node_list)

        # Put nodes in eligible nodes into a queue
        while(Q is not empty):
            # Pop an element from Q (i.e., a node)
        # Check secondary collisions
        for f in node_list[e.parendID].neighbors:
            aa
            # Check if f in eligible nodes?
            # Eligible_nodes.remove(f)
        # Check for primary collision:
            # Remove all nodes that cause primary collision with the transmission from e to e.parentID
        e.tx_time_slot = t

        t += 1
        
    # return t - return time after done scheduling
    
    pass