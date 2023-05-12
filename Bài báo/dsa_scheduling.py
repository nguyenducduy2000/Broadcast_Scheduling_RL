import queue
import sys
from libs import dtc_fas

INFINITY = sys.maxsize - 1

def dsa_scheduling(node_list, duty_cycle):
    """
    This implementation considers the active slot in range[0, 1, ... duty_cycle], while
    time t in range [0,1,2,...]
    to convert from t to the active slot, take [t% duty_cycle]

    :param node_list:
    :param duty_cycle:
    :return:
    """
    t = 0
    Sf = []
    node_set = set([i for i in range(0, len(node_list))])
    while len(Sf) < len(node_list) -1:  # we don't count sink node in
        #print len(Sf)
        eligible_nodes, scheduled_nodes = get_eligible_nodes(node_list, duty_cycle, t)
        #print eligible_nodes, scheduled_nodes
        non_leaf_nodes = node_set.difference(set(eligible_nodes+scheduled_nodes))
        weight_calc(node_list, eligible_nodes, non_leaf_nodes, t % duty_cycle)
        sorted_eligible_nodes = sorted(eligible_nodes, key=lambda x: node_list[x].dcat_weight, reverse=False)
        #print("at time slot", t, "candidate senders:", sorted_eligible_nodes)
        S = []
        R = []
        greedy_scheduling(node_list, sorted_eligible_nodes, S, R, duty_cycle, t)
        Sf += S
        t += 1
    pass


def dsa_scheduling_wo_dynamic(node_list, duty_cycle):
    """
    This function is different from the dsa_scheduling: it gives priority to the predefined parent in the initial
    tree, then if there are more nodes that can be scheduled ==> go by calling greedy_scheduling()
    :param node_list:
    :param duty_cycle:
    :return:
    """
    t = 0
    Sf = []
    node_set = set([i for i in range(0, len(node_list))])
    while len(Sf) < len(node_list) - 1:  # we don't count sink node in
        # print len(Sf)
        eligible_nodes, scheduled_nodes = get_eligible_nodes(node_list, duty_cycle, t)
        # print eligible_nodes, scheduled_nodes
        cand_parents = node_set.difference(set(scheduled_nodes))
        weight_calc(node_list, eligible_nodes, cand_parents, t % duty_cycle)
        sorted_eligible_nodes = sorted(eligible_nodes, key=lambda x: node_list[x].dcat_weight, reverse=True)

        S = []
        R = []
        greedy_scheduling_wo_dynamic(node_list, sorted_eligible_nodes, S, R, duty_cycle, t)
        #remaining_eligible_nodes = [x for x in sorted_eligible_nodes if x not in S]
        #greedy_scheduling(node_list, remaining_eligible_nodes, S, R, duty_cycle, t)
        Sf += S
        t += 1
    pass


def get_eligible_nodes(node_list, duty_cycle, time_now):
    """
    Eligible nodes consist of:
    - Nodes that are not assigned transmitting timeslot tx_wp
    - Nodes that all of its children got their tx_wp
    - max(tx_wp(childrenIDs)) * (duty_cycle-1) + active_timeslot(u) < time_now
    - must have at least one neighbor active at time_now
    :param node_list:
    :param duty_cycle:
    :param time_now:
    :return:
    """
    eligible_nodes = []
    scheduled = []
    for u in node_list:
        eligible = False
        if u.tx_wp == -1:  # u is not assigned a transmitting working period
            if len(u.childrenIDs) > 0:  # u has child(ren)
                for c in u.childrenIDs:
                    if node_list[c].tx_wp == -1:  # all of its children must have got tx_wp, else break and eligible = False
                        break
                else:
                    eligible = True
            else:
                eligible = True
        else:
            scheduled.append(u.ID)
        if eligible:
            if (max(u.rx_wp) - 1) * duty_cycle + u.timeslot < time_now: #  is u ready for transmitting? depend on its <rx_wp, active_timeslot>
                for ne in u.neighbors:
                    if node_list[ne].timeslot == time_now % duty_cycle and node_list[ne].tx_wp == -1:
                        eligible_nodes.append(u.ID)
                        break
    return eligible_nodes, scheduled


def weight_calc(node_list, eligible_nodes, cand_parents, timeslot):
    """
    returns the number of non-leaf neighbors which has active time slot = timeslot
    :param timeslot:
    :param node_list:
    :param eligible_nodes:
    :param cand_parents:
    :return:
    """
    for u in eligible_nodes:
        node_list[u].dcat_weight = 0
        for nu in node_list[u].neighbors:
            if nu in cand_parents and node_list[nu].timeslot == timeslot:
                node_list[u].dcat_weight += 1
    pass


def neighbors_of_a_set(node_list, a_set):
    """
    Return a list of neighbors of the nodes in 'a_set'
    :param node_list:
    :param a_set:
    :return:
    """
    neighbor_set = set([])
    for u in a_set:
        for v in node_list[u].neighbors:
            neighbor_set.add(v)
    return list(neighbor_set)


def greedy_scheduling(node_list, eligible_nodes, current_senders, current_receivers, duty_cycle, time_now):
    """
    This implements our scheduling algorithm:
        - Let all the sender freely choose its receiver regardless of its predefined parent in the initial tree
        - Each sender chooses the receiver that has smallest number of neighbors in the {remaining candidate senders}
    :param node_list: network data structure
    :param eligible_nodes: the list of candidate senders
    :param current_senders: the list of the scheduled senders in this current time slot
    :param current_receivers: the list of the receivers of the current_senders
    :param duty_cycle: the working period length (how many slots)
    :param time_now: the time slot now
    :return: None (after this function call, current_senders and current_receivers change and will be used in the main
            function)
    """
    eligible_queue = queue.Queue()
    for e in eligible_nodes:
        eligible_queue.put(e)
    while not eligible_queue.empty():
        u = eligible_queue.get()
        if u not in current_receivers:
            if u not in neighbors_of_a_set(node_list, current_receivers):
                r = None
                # here filter the neighbors of u that are not yet scheduled
                neighbors_of_u = [v for v in node_list[u].neighbors if node_list[v].tx_wp == -1]

                for p in neighbors_of_u:
                    if node_list[p].tx_wp == -1 and node_list[p].timeslot == time_now % duty_cycle:
                        if p not in neighbors_of_a_set(node_list, current_senders):
                            if r is None:
                                r = p
                            else:
                                neighbors_of_p = [x for x in node_list[p].neighbors if node_list[x].tx_wp == -1]
                                neighbors_of_r = [y for y in node_list[r].neighbors if node_list[y].tx_wp == -1]
                                if len(neighbors_of_p) < len(neighbors_of_r):
                                    r = p

                if r is not None:
                    p = node_list[u].parentID  # p becomes previous parent of node u
                    node_list[u].parentID = r
                    node_list[r].childrenIDs.append(u)
                    node_list[r].rx_wp.append(time_now // duty_cycle + 1)
                    node_list[p].childrenIDs.remove(u)  # node u has changed its parent

                    # ISELIGIBLE(p) in the paper:
                    # if node p does not have 'any unscheduled children left'
                    # if node p is not a receiver in the current round

                    if p not in current_receivers:
                        if len(node_list[p].childrenIDs) != 0:
                            for w in node_list[p].childrenIDs:
                                if node_list[w].tx_wp == -1:
                                    break

                            # if all the children have been scheduled
                            else:
                                if (max(node_list[p].rx_wp)-1) * duty_cycle + node_list[p].timeslot < time_now:
                                    eligible_queue.put(p)
                        else:
                            eligible_queue.put(p)

                    node_list[u].tx_wp = time_now // duty_cycle + 1
                    # print "node", u, "has been assigned time slot", j, node_list[u].timeslot
                    current_senders.append(u)
                    current_receivers.append(r)


def greedy_scheduling_wo_dynamic(node_list, eligible_nodes, current_senders, current_receivers, duty_cycle, time_now):
    """
    This function is different from the greedy_scheduling: it gives priority to the predefined parent in the initial
    tree, then if there are more nodes that can be scheduled ==> go by calling greedy_scheduling()
    :param node_list: network data structure
    :param eligible_nodes: the list of candidate senders
    :param current_senders: the list of the scheduled senders in this current time slot
    :param current_receivers: the list of the receivers of the current_senders
    :param duty_cycle: the working period length (how many slots)
    :param time_now: the time slot now
    :return: None (after this function call, current_senders and current_receivers change and will be used in the main
            function)
    """
    for u in eligible_nodes:
        if u not in neighbors_of_a_set(node_list, current_receivers):
            parent = node_list[u].parentID
            slot = time_now % duty_cycle
            if node_list[parent].timeslot == slot:
                if parent not in neighbors_of_a_set(node_list, current_senders):
                    current_wp = time_now // duty_cycle + 1
                    if current_wp not in node_list[parent].rx_wp:
                        node_list[u].tx_wp = current_wp
                        node_list[node_list[u].parentID].rx_wp.append(current_wp)
                        current_senders.append(u)
                        current_receivers.append(node_list[u].parentID)
    pass



def dijkstra_duty_cycle(node_list, dutycycle):
    """
    building a Shortest Path Tree using Dijkstra algorithm, with link cost is the duty cycle delay
    :param node_list:
    :param dutycycle:
    :return:
    """
    q = []
    for i in range(0, len(node_list)):
        node_list[i].distance = INFINITY
        q.append(i)
    node_list[0].distance = 0
    while len(q) > 0:
        receiver = min(q, key=lambda x: node_list[x].distance)
        q.remove(receiver)
        for sender in node_list[receiver].neighbors:
            alt = node_list[receiver].distance + dtc_fas.delay(node_list, sender, receiver, dutycycle)
            if alt < node_list[sender].distance:
                node_list[sender].distance = alt
                node_list[sender].parentID = receiver

    for i in range(0, len(node_list)):
        if node_list[i].parentID is not None:
            u = node_list[i].parentID
            node_list[u].childrenIDs.append(i)
        else:
            # print(node_list[i].ID)  # root node
            pass
