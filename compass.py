# compass.py: (c) William Menz (wjm34) 2012

# Global imports
import sys
import getopt
import os

# Project-specific imports
import mopsrun.mopsrun

# Default initialisations
auto = True         # Automatically look in current working dir?
rundir = ""         # Directory for calculation

# Define usage
def usage():
    print("compass postprocessor for MOPS, (c) wjm34 2012. Usage:")
    print("python compass.py [args]")
    print("\t-d <dir>: find run in directory <full or relative path>")




#*********************************************************************
# MAIN PROGRAM BODY
#*********************************************************************

# Check program arguments
try:
    opts, args = getopt.getopt(sys.argv[1:],"h:d:",["help"]) 
except getopt.GetoptError:
    usage()
    sys.exit(1)
for opt, arg in opts:
    if opt in ["-h", "--help"]:      
        usage()
        sys.exit()
    elif opt == "-d":
        rundir = arg
        print("compass: looking in directory {0}.".format(rundir))
        auto = False
    else:
        usage()
        sys.exit(2)

# Initialise a new MopsRun object
mopsoutput = mopsrun.mopsrun.MopsRun()

# Locate the MOPS output files in the current working directory
if auto:
    mopsoutput.findMopsRun()
else:
    # Check if directory exists first.
    if os.path.exists(rundir):
        print("compass: changing to directory {0}".format(rundir))
        os.chdir(rundir)
        mopsoutput.findMopsRun()
    else:
        print("compass: specified directory not found.")
        sys.exit(2)

# Check if sufficient info has been found
if (not mopsoutput.enoughInfo()):
    print("compass: MOPS results not found.")
    sys.exit(3)

# Initialise the MopsRun with the data found
mopsoutput.initialise()
