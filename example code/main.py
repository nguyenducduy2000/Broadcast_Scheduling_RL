import node
import trees
import random
import math

def distance (node1, node2):
    print("distance: " + str(math.sqrt(pow((node1.x-node2.x), 2) + pow((node1.y-node2.y), 2))))
    return math.sqrt(pow((node1.x-node2.x), 2) + pow((node1.y-node2.y), 2))


if __name__ == "__main__":
    # Generate a list of nodes
    X = 200  # X-dimension
    Y = 200  # Y-dimension
    R = 30   # communication range
    N = 400 # number of nodes

    node_list = []
    for i in range(0, N):
        # generate a node
        node = node.Node()
        node.ID = i
        node.x = random.randint(0, 200)
        node.y = random.randint(0,200)
    
        # check duplication?
        for k in node_list:
            if k.x != node.x and k.y != node.y:
                continue
            else:
                print("collision")
                node.x = random.unform(0,200)
                node.y = random.uniform(0,200)
        
        node_list.append(node)
        pass

    # Update neighbors
    # loop through node_list
    # check distance < 30
    # node_list[i].neighbors.append(<id>)

    # Build a tree on the node_list


    # Do some scheduling algorithm
    # Iterative
    # Per time slot: get eligible nodes (nodes that can be scheduled--> exclude scheduled nodes and..?)
    # 
    pass