import random
from collections import Counter

consensus_values = [0,1]

class Node:
    def __init__(self, id, value=None, peer_connections=9, rounds=10, peers=[], alpha=0.5):
        self.id = id
        self.value = value
        self.peer_connections = peer_connections
        self.rounds = rounds
        self.peers = peers
        self.alpha = alpha

    def on_query(self, value):
        if self.value is None:
            self.value = value
        return self.value

    def slush_query(self, all_nodes):
        self.peers = random.sample(all_nodes, self.peer_connections)
        value_estimate = [ peer.on_query(self.value) for peer in self.peers ]
        self.counter = Counter(value_estimate)
        return self.counter, self.slush_result()

    def slush_result(self):
        for value in self.counter:
            if self.counter[value] > self.alpha*self.peer_connections:
                return value
        raise Exception("slush_result did not return any value!")

    def slush_update(self):
        self.value = self.slush_result()
        return self.value

    '''
    def slush_loop(self, all_nodes):
        for round in range(self.rounds):
            if self.value is None:
                continue
            self.slush_query(all_nodes)
            self.slush_update()
        return self.value
    '''

all_nodes = [Node(x, random.choice(consensus_values)) for x in range(10000)]

def see_split():
    value_counter = {}
    for value in consensus_values:
        value_counter[value] = 0
    for node in all_nodes:
        value_counter[node.value] += 1
    return value_counter

def run_slush_round():
    for node in all_nodes:
        node.slush_query(all_nodes)
    for node in all_nodes:
        node.slush_update()
    return see_split()

print(see_split())

for round in range(10):
    print(run_slush_round())
