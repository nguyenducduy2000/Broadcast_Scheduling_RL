"""@package docstring
Programmed by Dzung T. Nguyen @SKKU, Korea
Data structure of a network node
"""

# energy consumption in mW (WSN SIMULATORS EVALUATION: AN APPROACH
# FOCUSING ON ENERGY AWARENESS-Michel Bakni)
e_tx = 52
e_rx = 59
e_sleeping = 0.06
e_active_idle = 0.06


class Node:
    # The constructor
    def __init__(self, node_id=0, x=0.0, y=0.0, timeslot=-1):
        # ID of a node
        self.ID = node_id
        # x-axis position
        self.x = x
        # y-axis position
        self.y = y
        # ID of the parent
        self.parentID = None
        # list of children
        self.childrenIDs = []
        # list of neighbors
        self.neighbors = []
        # active time slot
        self.timeslot = timeslot
        # assigned transmitting working period
        self.tx_wp = -1
        # cycle
        self.cycle = -1
        # distance from the source, for building a BFS Tree
        self.distance = 100000
        # lower bound of aggregation time to a node (# working period), considering primary collisions only
        self.lb_agg_wp = -1

        self.cw_dedas = 0  # for dedas scheme
        # for 2016 scheme leaf scheduling
        self.latency_connector_mis = [-1, -1, -1]  # min-latency / mis_node / connector
        self.sdu = -1
        self.tuv = -1

        self.layer = -1  # layer in the SPT
        self.layer_cds = -1  # layer in the dtc_fas scheme
        self.is_dominator = False
        self.is_connector = False
        self.distance_to_prev_dominator = -1
        self.connector = None
        self.prev_dominator = None
        self.next_layer_neighbors = []
        self.prev_layer_neighbors = []
        # list of working periods that this node will receive data
        # note: in the original pseudocode, the author only store the highest working period
        # we are keeping track of all
        self.rx_wp = [0]
        # list of working periods that this node will hear other transmissions
        self.overhearing = []

        self.dcat_weight = 0

        self.added = 0
        # for constructing dfs tree:
        self.discovered = False

        self.mat_dc = -1  # for MAT calculation for duty cycle network
