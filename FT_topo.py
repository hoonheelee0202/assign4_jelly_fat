from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf, TCLink
from mininet.util import dumpNodeConnections
from mininet.nodelib import LinuxBridge
import os

class Fattree (Topo):
    
    def build(self, k=4):

        
        
        self.CoreSwitchList = []
        self.AggSwitchList = []
        self.EdgeSwitchList = []
        self.HostList = []

        self.pod = k
        # the number of pods = k = 4
        self.iCoreLayerSwitch = (k/2)**2
        # the number of core switches = (k/2)^2 = 4
        self.iAggLayerSwitch = k*k/2
        # the number of aggregation = k*k/2 = 8
        self.iEdgeLayerSwitch = k*k/2
        # the number of edge = k*k/2 = 8
        self.iHost = k**3/4
        # the number of total hosts = k^(3/4) = 16

        #Init Topo
        #Topo.__init__(self)

        
        """
        Add switch and host
        we have 20 switches and 16 hosts
        
        """
        self.createTopo()
        
        self.createLink(bw_c2a=0.2, bw_a2e=0.1, bw_h2a=0.05)
        
    def createTopo(self):
        self.createCoreLayerSwitch(self.iCoreLayerSwitch)
        self.createAggLayerSwitch(self.iAggLayerSwitch)
        self.createEdgeLayerSwitch(self.iEdgeLayerSwitch)
        self.createHost(self.iHost, self.pod)  

    
    def createCoreLayerSwitch(self, NUMBER):
        print "Create Core Layer"
        self._addSwitch(NUMBER, 1, self.CoreSwitchList)


    def createAggLayerSwitch(self, NUMBER):
        print"Create Aggregation Switch"
        self._addSwitch(NUMBER, 2, self.AggSwitchList)


    def createEdgeLayerSwitch(self, NUMBER):
        print"Create Edge Switch"
        self._addSwitch(NUMBER, 3, self.EdgeSwitchList)
    
    def _addSwitch(self, number, level, switch_list):
        for x in xrange(1, number+1):
            S_L = str(level) + "--"
            if x >= int(10):
                S_L = str(level) + "-"
            switch_list.append(self.addSwitch('s{}'.format(S_L + str(x)),cls=LinuxBridge,stp=1))
            printf = "No. %s Switch is at %s level" %(str(x),str(level))
            print printf


    def createHost(self, NUMBER, pod):
        mount = 1
        for p in xrange(0, pod):
            for w in xrange(pod/2, pod):
                for h in xrange(2, pod/2+2):
                    Host = self.addHost('h{}'.format(mount))
                    self.HostList.append(Host)
                    mount += 1

    

    """
    Add Link:
    c2a = core to aggregation
    a2e = aggregation to edge
    h2a = hosts to aggregation
    """
    def createLink(self,bw_c2a=0.2, bw_a2e=0.1, bw_h2a=0.05):

        print "Add link Core to Aggregation."

        for i in xrange(self.pod**2/4):
            x = i/(self.pod/2) 
            mount = 0
            for j in xrange(self.pod):
                up = self.CoreSwitchList[i]
                down = self.AggSwitchList[x + mount*(self.pod/2)]
                #self.addLink(up, down, bw=bw_c2a)
                self.addLink(up, down)
                mount += 1
        
        print "Add link Aggregation to Edge."

        for i in xrange(self.pod**2/2):
            x = i/(self.pod/2)
            for j in xrange(self.pod/2):
                up = self.AggSwitchList[i]
                down = self.EdgeSwitchList[x*(self.pod/2) + j]
                #self.addLink(up, down, bw=bw_a2e)
                self.addLink(up, down)
        
        print "Add link Edge to Host."
        x = 0
        for i in xrange(self.pod**2/2):
            for j in xrange(self.pod/2):
                up = self.EdgeSwitchList[i]
                down = self.HostList[x*(self.pod/2) + j]
                #self.addLink(up, down, bw=bw_h2a)
                self.addLink(up, down)
            x += 1
            
        
    
    
