# compass.py: (c) William Menz (wjm34) 2012

# Global imports
import sys
import getopt
import os

# Project-specific imports
import mopsrun.mopsrun
import mopsrun.mopsparser

# Default initialisations
auto = False

# Define usage
def usage():
    print("compass postprocessor, (c) wjm34 2012. Usage:")
    print("\t-a: automatically find files")




#*********************************************************************
# MAIN PROGRAM BODY
#*********************************************************************

# Check program arguments
try:
    opts, args = getopt.getopt(sys.argv[1:],"h:a",["help"]) 
except getopt.GetoptError:
    usage()
    sys.exit(1)
for opt, arg in opts:
    if opt in ["-h", "--help"]:      
        usage()
        sys.exit()
    elif opt == "-a":
        print("compass: searching for MOPS run")
        auto = True
    else:
      usage()
      sys.exit(2)

# Initialise a new MopsRun object
mopsoutput = mopsrun.mopsrun.MopsRun()

# Locate the MOPS output files
if auto:
    mopsoutput.findMopsRun()
else:
    print("compass: currently unsupported.")
    sys.exit(3)

# Check if sufficient info has been found
if (not mopsoutput.enoughInfo()):
    print("compass: MOPS results not found.")
    sys.exit(3)

# Initialise the MopsRun with the data found
mopsoutput.initialise()
