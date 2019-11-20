#!/usr/bin/python
import os              # OS level utilities
import sys
import argparse   # for command line parsing

from signal import SIGINT
from time import time

import subprocess

# These are all Mininet-specific
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import CLI
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.util import pmonitor
from mininet.node import Controller, RemoteController
# This is our topology class created specially for Mininet
from FT_topo import Fattree

##################################
def genCommandsFile (hosts, args):
    try:
        # first remove any existing out files
        for i in range (len (hosts)):
            # check if the output file exists
            if (os.path.isfile (hosts[i].name+".out")):
                os.remove (hosts[i].name+".out")

        # create the commands file. It will overwrite any previous file with the
        # same name.
        cmds = open ("commands.txt", "w")

        # @NOTE@: You might need to make appropriate changes
        #                          to this logic by using the right file name and
        #                          arguments. My thinking is that the map and
        #                          reduce workers can be run as shown unless
        #                          you modify the command line params.

        # @NOTE@: for now I have commented the following line so we will have to
        # start the master manually on host h1s1

        # first create the command for the master
        #cmd_str = hosts[0].name + " python mr_wordcount.py -p " + str (args.masterport) + " -m " + str (args.map) + " -r " + str (args.reduce) + " " + args.datafile + " &> " + hosts[0].name + ".out &\n"
        #cmds.write (cmd_str)

        #  next create the command for the map workers
        for i in range (args.map):
            cmd_str = hosts[i+1].name + " python mr_mapworker.py " + hosts[0].IP () + " " + str (args.masterport) + " &> " + hosts[i+1].name + ".out &\n"
            cmds.write (cmd_str)

        #  next create the command for the reduce workers
        k = 1 + args.map   # starting index for reducer hosts (master + maps)
        for i in range (args.reduce):
            cmd_str = hosts[k+i].name + " python mr_reduceworker.py " + hosts[0].IP () + " " + str (args.masterport) + " &> " + hosts[k+i].name + ".out &\n"
            cmds.write (cmd_str)

        # close the commands file.
        cmds.close ()
    except:
            print "Unexpected error in run mininet:", sys.exc_info()[0]
            raise


def main ():
    
    "Create and run the Wordcount mapreduce program in Mininet topology"
    
    # instantiate our topology
    print "Instantiate topology"
    topo = Fattree(4)
    # k = 4 in this case
    #topo.createTopo()
    #
    #topo.createLink()
    # create link between hosts and switches
    net = Mininet(topo=topo, link=TCLink, autoSetMacs=True,autoStaticArp=True)

    #net.addController('Controller', port=5557)

    net.start()

    # debugging purposes
    print "Dumping host connections"
    dumpNodeConnections (net.hosts)

    
    
    #genCommandsFile (net.hosts, parsed_args)

    # run the cli
    #print "Testing network connectivity"
   
    CLI (net)

    # @NOTE@
    # You should run the generated commands by going to the
    # Mininet prompt on the CLI and typing:
    #     source commands.txt
    # Then, keep checking if all python jobs (except one) are completed
    # You can look at the *.out files which have all the debugging data
    # If there are errors in running the python code, these will also
    # show up in the *.out files.
    
    # cleanup
    #net.pingAll()    
    net.stop ()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    main ()
