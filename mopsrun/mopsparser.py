# mopsparser.py: (c) William Menz (wjm34) 2012

# Global imports
import ensemble
import trajectory
import re

class Parser:
    # Default constructor
    def __init__(self, fname):
        self.fname = fname
        print("compass: loading file {0}.".format(fname))
    
    
    # Opens the CSV and returns the stream
    def openCSV(self):
        self.istream = open(self.fname, "r")
    
    # Closes the CSV
    def closeCSV(self):
        self.istream.close()
    
    # Reads a CSV line and converts all to float
    def getCSVLine(self, csvline, datatype):
        
        # Split on comma delimiter
        line = csvline.split(',')
        
        # Remove any \n characters
        cleanline = []
        for l in line:
            
            # Convert to floats
            if (datatype == type(1.0)):
                cleanline.append(float(l.strip()))
            elif (datatype == type("str")):
                cleanline.append(str(l.strip()))
            else:
                print("compass: unrecognised data type")
                
        return cleanline
    
    # Returns a parameter's name and unit as vector
    def getParameterName(self, string):
        
        try:
            splitstring = string.split('(')
            unit = splitstring[1].split(')')[0]
            param = splitstring[0].strip()
        except:
            print("compass: no unit found for parameter {0}".format(string))
            param = string
            unit = "-"
        
        return [param, unit]
        
# Class to parse -psl.csv files for a particle ensemble
class ParserPSL(Parser):
    # Default constructor
    def __init__(self, fname):
        self.fname = fname
        print("compass: loading file {0}.".format(fname))
        
        # Get headers of PSL
        self.openCSV()
        self.headers = self.getPSLHeaders()
        
    
    # Get the time at which the PSL was printed
    def getPSLTime(self):
        
        # Split on either side of the brackets
        rhs = self.fname.split('(')[1]
        lhs = rhs.split(')')[0]
        
        timestr = lhs.split('s')[0]
        return float(timestr)
    
    # Called on input stream to find the headers
    def getPSLHeaders(self):
        csvline = self.istream.readline()
        
        headers = self.getCSVLine(csvline, type("str"))
        
        return headers
    
    # Returns a stream of parsed particle information to construct a particle
    def getParticleLine(self):
        
        # Load the line
        csvline = self.istream.readline()
        line = self.getCSVLine(csvline, type(1.0))
        
        # Return the new particle
        return line
    
    # Returns the full block of parsed particle data
    def getEnsembleData(self):
        data = []
        
        # Load the line
        for csvline in self.istream:
            line = self.getCSVLine(csvline, type(1.0))
            data.append(line)
        
        # Now close the data file
        self.closeCSV()
        
        # Return the new particle
        return data        
    
    # Uses the particle headers to create a dictionary of parameters
    def getParameterDictionary(self):
        
        newdict = {}
        
        # Loop over headers to add to dictionary
        i = 0
        while i < len(self.headers):
            newdict[i] = self.getParameterName(self.headers[i])
            i += 1
        
        return newdict

# Class to parser rate or chemistry-like temporal evolution trajectories
class ParserTrajectory(Parser):
    # Default constructor
    def __init__(self, fname):
        self.fname = fname
        print("compass: loading file {0}.".format(fname))

        # Get headers of trajectory
        self.openCSV()
        self.getTrajectoryHeaders()
        
    # Determine the headers of the trajectory
    def getTrajectoryHeaders(self):
        csvline = self.istream.readline()
        
        self.headers = self.getCSVLine(csvline, type("str"))
    
    # Changes the headers into parameter names [paramnames, units]
    def getTrajectoryNames(self):
        names = []
        
        # Loop over headers to find names
        i = 2
        while i < len(self.headers):
            if i % 2 == 0:
                names.append(self.getParameterName(self.headers[i]))
            i+=1
        
        return names
    
    # Reads the ensemble data
    def getTrajectoryData(self):
        data = []
        
        # Loop over the input stream
        for csvline in self.istream:
            data.append(self.getCSVLine(csvline, type(1.0)))
        
        return data
    
    # Convert raw trajectory data into [time value error] arrays
    def getAllTrajectories(self, trajectory_names):
        data = self.getTrajectoryData()
        
        # This generates data in the form [step time param1 err1 param2 err2]
        steps = []
        times = []
        
        # Initialise array for processed data
        values = []
        errors = []
        for n in trajectory_names:
            values.append([])
            errors.append([])
        
        # Loop over the the rows of data
        for line in data:
            
            # Loop over the rows of the line
            i = 0
            while i < (len(line) - 1):
                if i == 0:
                    steps.append(line[i])
                elif i == 1:
                    times.append(line[i])
                elif i % 2 == 0:
                    values[(i-2)/2].append(line[i])
                    errors[(i-2)/2].append(line[i+1])
                i += 1
        
        # Now have array of [[val1, err1], [val2, err2]]
        newtrajectories = []  # Initialise storage for trajectory
        
        # Loop over process names and processed data
        for n, v, e in zip(trajectory_names, values, errors):
            newtrajectories.append(trajectory.Trajectory(n, times, v, e))
        
        return newtrajectories
        