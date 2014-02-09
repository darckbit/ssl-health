#!/usr/bin/python
#Main imports
import sys, getopt, os, tests

from printer import Printer
from test import Test
from service import Service
from health_assessor import HealthAssessor
from environment import Environment
from tests import *
from printers import *

# Version
VERSION = "0.1"


# Main function
def main():

    # Check for config file
    if not os.path.exists('config.py'):
        print "Please provide a config."
        exit(4)

    import config


    # Read args.
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:vp:m", ["host=", "help", "printer=", "verbose", "version", "tmpfolder=", "multi", "doNotClearCache"])
    except getopt.GetoptError as err:
        print str(err) 
        usage()
        sys.exit(2)
    
    output = "tui"
    verbose = False
    hosts = []
    multi = False
    for o, a in opts:
        if o in ("-v", "--verbose"):
            verbose = True
        elif o in ("-h", "--host"):
            hosts.append(a)
        elif o in ("-p", "--printer"):
            output = a
        elif o == "--version" :
            print "Version v" + VERSION
        elif o in ("-m", "--multi"):
            multi = True
        else:
            print o
            assert False, "unhandled option"

    if len(hosts) > 0:
        env = Environment(config)

        try:
            sys.modules["printers."+output]
        except KeyError:
            print "Printer not found. Exitting"
            sys.exit(3)

        printer = sys.modules["printers."+output].Printer()
        

        assessor = HealthAssessor(printer)

        for host in hosts:
            host_split = host.split(":")
            if len(host_split) == 1:
                host_split.append("443")
            assessor.addService(Service(host_split[0], host_split[1], env))
        
        for test in sorted(tests.__all__):
            if test not in ["__init__", "example"]:
                assessor.addTest(sys.modules["tests."+test].Test())
        if multi == True:
            assessor.threadBasedTestService()
        else:
            assessor.run()

def usage():
    print "Usage: ssl-health-assessor [OPTIONS]"
    print
    print "\t-h/--host\t- Host"
    print "\t-p/--printer\t- Printer (tui)"
    print "\t-v/--verbose\t- Verbose mode"
    print "\t-m/--multi\t- Experimental multi-threading"
    print "\t--version\t- Display Version"

def header():
    print "#" * 29
    print "#    SSL Health Assessor    #"
    print "#" * 29

if __name__ == "__main__":
    main()