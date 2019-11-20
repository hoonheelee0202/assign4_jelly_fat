from graph import NXTopology
import os
import sys
import networkx as nx
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.node import OVSController
from mininet.node import Controller
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.clean import Cleanup
from mininet.nodelib import LinuxBridge
#sys.path.append("../../")
#from jelly_pox import JELLYPOX
from subprocess import Popen
from time import sleep, time
from mininet.util import dumpNodeConnections,pmonitor
import hashlib

from itertools import islice
from mininet.log import setLogLevel
import pickle
import random

# Topology port description:
# Every switch with switch_id=i is connected to host_id by port "number_of_racks + host_id"
#                               is connected to switch j by port "j"

src_dest_to_next_hop = {} # d1 maps (src_switch_id, dest_switch_id, current_switch_id) to [next_switch_id1, next_switch_id2, ...]
host_ip_to_host_name = {} # d2 e.g. maps '10.0.0.1' to 'h0'

######################################### Parameters #########################################
iperf_time = 100 # seconds
switch_switch_link_bw = 400 # Mbps
switch_host_link_bw = 100 # Mbps
#r_method = '8_shortest' # 'ecmp8', 'ecmp64' or '8_shortest'
#number_of_tcp_flows = 1 # should be 1 or 8
#nx_topology = NXTopology(number_of_servers=100, switch_graph_degree=3, number_of_links=15)
##############################################################################################

class JF_Topo(Topo):

    def build(self,number_of_servers, switch_graph_degree, number_of_links):

        nx_topology = NXTopology(number_of_servers, switch_graph_degree, number_of_links)
        
        # create switches
        for n in nx_topology.G.nodes():
            self.addSwitch('s'+str(n+1),cls=LinuxBridge,stp=1)
        
        # connect switches to each other
        
        # for every link (i,j), switch with switch_id=i is connected to port number i of switch with switch_id=j
        for e in nx_topology.G.edges():
            self.addLink('s'+str(e[0]+1), 's'+str(e[1]+1), e[1]+1, e[0]+1, bw=switch_switch_link_bw)
        
        # create hosts and connect them to ToR switch
        for h in range(nx_topology.number_of_servers):
            self.addHost('h'+str(h))
            self.addLink('h'+str(h), 's'+str(nx_topology.get_rack_index(h)+1), 0, nx_topology.number_of_racks + h+1, bw=switch_host_link_bw)

