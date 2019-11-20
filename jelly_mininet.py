#!/usr/bin/python

#
# Vanderbilt University, Computer Science
# CS4287-5287: Principles of Cloud Computing
# Author: Aniruddha Gokhale
# Created: Nov 2016
# 
#  Purpose: The code here is used to demonstrate the homegrown wordcount
# MapReduce framework on a network topology created using Mininet SDN emulator
#
# The mininet part is based on examples from the mininet distribution. The MapReduce
# part has been modified from the earlier thread-based implementation to a more
# process-based implementation required for this sample code
#

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
from jelly_pox import JELLYPOX
import networkx as nx
# This is our topology class created specially for Mininet
from jelly_topo import JF_Topo

##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()

    # @NOTE@: You might need to make appropriate changes
    #                          to this logic. Just make sure.

    # add optional arguments
    parser.add_argument ("-hs", "--nServers", type=int, default=16, action="store", help="Number of servers")
    parser.add_argument ("-sw", "--nSwitches", type=int, default=20, action="store", help="Number of switches")
    parser.add_argument ("-po", "--nPorts", type=int, default=4, action="store", help="Number of ports per switch")


    # parse the args
    args = parser.parse_args ()

    return args
    
##################################
# Save the IP addresses of each host in our network
##################################
def saveIPAddresses (hosts, file="ipaddr.txt"):
    # for each host in the list, print its IP address in a file
    # The idea is that this file is now provided to the Wordcount
    # master program so it can use it to find the IP addresses of the
    # Map and Reduce worker machines
    try:
        file = open ("ipaddr.txt", "w")
        for h in hosts:
            file.write (h.IP () + "\n")

        file.close ()
        
    except:
            print "Unexpected error:", sys.exc_info()[0]
            raise


##################################
#  Generate the commands file to be sources
#
# @NOTE@: You will need to make appropriate changes
#                          to this logic.
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
        #         to this logic by using the right file name and
        #                          arguments. My thinking is that the map and
        #                          reduce workers can be run as shown unless
        #                          you modify the command line params.

        # @NOTE@: for now I have commented the following line so we will have to
        #         start the master manually on host h1s1

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

######################
# main program
######################
def main ():
    "Create and run the Wordcount mapreduce program in Mininet topology"

    # parse the command line
    parsed_args = parseCmdLineArgs ()
    
    # instantiate our topology
    print "Instantiate topology"
    
    topo = JF_Topo(number_of_servers=parsed_args.nServers, switch_graph_degree=parsed_args.nSwitches, number_of_links=parsed_args.nPorts)
    
    

    # create the network
    print "Instantiate network"
    #net = Mininet (topo, link=TCLink)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink,controller=JELLYPOX,autoSetMacs=True)
    # activate the network
    print "Activate network"
    net.start ()

    # debugging purposes
    print "Dumping host connections"
    dumpNodeConnections (net.hosts)

    #print "Generating commands file to be sourced"
    #genCommandsFile (net.hosts, parsed_args)

    # run the cli
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
    net.stop ()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    main ()