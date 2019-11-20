
import networkx as nx
from itertools import islice
import numpy as np
import random


class NXTopology:
    
    def __init__(self, number_of_servers, switch_graph_degree, number_of_links):
        
        self.number_of_servers = number_of_servers
        self.switch_graph_degree = switch_graph_degree  # k
        self.number_of_racks = (2 * number_of_links) // self.switch_graph_degree

        print("number_of_rack = " + str(self.number_of_racks))
        self.number_of_servers_in_rack = int(np.ceil(float(self.number_of_servers) / self.number_of_racks))
        self.number_of_switch_ports = self.number_of_servers_in_rack + self.switch_graph_degree  # r
        
        self.G = nx.random_regular_graph(self.switch_graph_degree, self.number_of_racks)
        #d (int) - The
        #  degree of each node.
        
        #n (integer) - The number of nodes. The value of n * d must be even.

        print("number_of_servers_in_rack = " + str(self.number_of_servers_in_rack))
        print("number_of_switch_ports = " + str(self.number_of_switch_ports))
        print("RRG has " + str(self.number_of_racks) + " nodes with degree " + str(self.switch_graph_degree) + " and " + str(self.G.number_of_edges()) + " edges")
    
    def get_rack_index(self, server_index):
        return server_index % self.number_of_racks
    