#!/usr/bin/python2

import sys
import argparse
import getopt
import os

#First: we write what the program is and how to use it.
parser = argparse.ArgumentParser(description='The aim of this script is to produce individual stats from the game www.goldenboboys.fr.\nGraphs are available in the graphs folder.')
parser.add_argument("-n", "--name", required=True, action="store", type=str, help="The username for your account on Goldenboys.")
parser.add_argument("-p", "--password", required=True, action="store", type=str, help="The password for your account on Goldenboys.")
parser.add_argument("-o", "--output", action="store", type=str, help="The name of the output graph (+'.png' at the end). By default, it's username.")
parser.add_argument("-v", action="version", version="%(prog)s 1.0")

#After, we catch arguments
args = parser.parse_args()

#We define the name of the output graph. By default: the user name.
if not args.output:
	output = args.name
else:
	output = args.output

#Bouh... We use a file for sending user's identity to the scrapy's script.
#I haven't find a better was to do... #ShameOnMe!!!
stamp = open("stp", "wt")
stamp.write(args.name + ':' + args.password + ':' + output)
stamp.close()

#We only continue the execution if has give a username and a password.
#if not name or not password:
#	usage()
#	sys.exit(1)

#Execution of the crawler, that will also make the graph.
os.system("scrapy crawl gb")
